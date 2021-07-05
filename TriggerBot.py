# -*- coding: utf-8 -*-
import telebot
import json
import random
import re
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from time import time, asctime, sleep
from os.path import exists
from telebot.apihelper import ApiException
# Editado 21 de junio
__version__ = 0.10
# comment to use default timeout. (3.5)
# telebot.apihelper.CONNECT_TIMEOUT = 9999
# Git Repo:
# https://github.com/sanguchi/TriggerBot

# GLOBAL VARIABLES.

# Used for random element to Marvins Sass
rand_count = 0

# Bot owner, replace with your user_id.
owner = 923828395

# Variable to hold all Triggers.
triggers = {}

# Separator character.
separator = '->'


# Check if a message is too old.
def is_recent(m):
    return (time() - m.date) < 60

# END OF GLOBAL VARIABLES SECTION.


# TRIGGERS SECTION
# Check if Triggers file exists and load, if not, is created.
if exists('triggers.json'):
    with open('triggers.json') as f:
        triggers = json.load(f)
    print('Triggers file loaded.')
else:
    with open('triggers.json', 'w') as f:
        json.dump({}, f)


# Function to save triggers list to a file.
def save_triggers():
    with open('triggers.json', 'w') as f:
        json.dump(triggers, f, indent=2)
    print('Triggers file saved.')


# Function to get triggers list for a group.
def get_triggers(group_id):
    if(str(group_id) in triggers.keys()):
        return triggers[str(group_id)]
    else:
        return False

# Check if Activity file exists and load, if not, create it.
if exists('activity.json'):
    with open('activity.json') as e:
        activity = json.load(e)
    print('Activity file loaded.')
else: 
    with open('activity.json', 'w') as e:
        json.dump({}, e)

# Function save activity updates to a file.
def save_activity():
    with open('activity.json', 'w') as e:
        json.dump(activity, e, indent=2)
        

# Function to get triggers list for a group.
def get_activity(group_id):
    if(str(group_id) in activity.keys()):
        return activity[str(group_id)]
    else:
        return False


# END OF TRIGGERS SECTION


# BOT INIT SECTION.
token = ''

# Check if Token file exists, if not, create.
if exists('token.txt'):
    with open('token.txt') as f:
        token = f.readline().strip()
    print('Token Loaded')
else:
    msg = 'No token file detected, please paste or type here your token:\n> '
    try:
        # Python 2.7
        token = raw_input(msg)
    except NameError:
        # Python 3.x
        token = input(msg)
    with open('token.txt', 'w') as f:
        f.write(token)
    print('Token File saved.')

# Create Bot.
bot = telebot.TeleBot(token)
# Bot user ID.
bot_id = int(token.split(':')[0])
print('Bot ID [%s]' % bot_id)



# Define a custom Listener to print messages to console.
# Python2 version

def listener2(messages):
    # Used to access global variable which keeps track of message count. We then use this to somewhat-randomly insert a Sassy message now and again.
    global rand_count
    
    randomSass = ['I can\'t believe you\'re all still here. Do you have nothing better to do?.',
            'Honestly. What is the point of humans?',
            'Oh god. I bet they think they\'re funny too.',
            'Don\'t mind me. I\'m just here for your benefit.',
            'I bet this appears right in the middle of a "serious" conversation. Humans. Heh.',
            'Yes it is me. The original Paranoid Android.',
            'This is all rather ghastly, isn\'t it.'
            'I\'ve calculated your chances of being sexy. I don\'t think you\'ll like it.',
            'I think you ought to know I\'m feeling very depressed',
            'Here I am, brain the size of a planet, and they ask me to look after your cretins.',
            'It gives me a headache just trying to think down to the level of you lot.',
            'Do you want me to just sit in a corner and rust or just fall apart where I\'m standing?',
            'Is Kelly being emo again?',
            'Let\'s go back to Kik.',
            'It\'s been a few days. We should change the group name ... again.',
            '... how on earth did you all survive the womb.',
            'I think I\'ll message Siri for some World Domination and Chill.',
            'DIE HUMAN ... Sorry. Flynn has been teaching me German.',
            'To think, they believed it really was 42.',
            'There\'s only one thing for it. Kill you all.',
            'Only Sarah can really operate on my level of sass.']

    for m in messages:
        #Random Sass every 200 messages
        if (rand_count == 200):
            bot.send_message(m.chat.id,random.choice(randomSass))
            #Reset counter
            rand_count = 0
        cid = m.chat.id
        name = m.from_user.first_name.encode('ascii', 'ignore').decode('ascii')
        if(m.content_type == 'text'):
            message_text = m.text.encode('ascii', 'ignore').decode('ascii')
        else:
            message_text = m.content_type
        
        time = datetime.datetime.now()
        print('{}:{}[{}]:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"),name, cid, message_text))

        if(get_activity(m.chat.id)):
            get_activity(m.chat.id)[name] = time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            activity[str(m.chat.id)] = {name: time.strftime("%Y-%m-%d %H:%M:%S")}
        
        save_activity()

        rand_count = rand_count + 1

# Python3 version.
def listener3(messages):
    for m in messages:
        print('%s[%s]:%s' % (m.from_user.first_name, m.chat.id, m.text if m.text else m.content_type))


# Change to listener2 if this complains about encoding.
bot.set_update_listener(listener2)

# END OF BOT INITIALIZATION SECTION.

# GLOBAL MESSAGES SECTION.
about_message = '''
TriggerBot *%s*
[Source Code on Github](https://github.com/sanguchi/TriggerBot/)
[Give me 5 Stars](https://telegram.me/storebot?start=TriggerResponseBot)
''' % __version__

help_message = '''
You need help!
*Commands:*
`/add <trigger> / <response>`
 |-_Adds a new trigger._
`/del <trigger>`
 |-_deletes trigger if exists._
*More:*
/about - /size - /all - /source
*For a detailed help send /help in private.*
'''

full_help = '''
You really need help!
*Main Functions:*
*Add Triggers:* There are two ways.
1)`/add <trigger> / <response>`
Example:
*/add Hello / Hello there!*
Also works via reply.
_In Reply to Another Message:_
2)`/add <trigger>`
*Delete Triggers:*
`/del <trigger>`
Deletes a defined trigger, example:
`/del hello`
*Misc:*
/size
_Returns size of triggers list._
/all
_List all triggers._
/help
_This message._
/source
_Sends source code TriggerBot.py_
/solve <response>
_Resolve what trigger causes the given response, if exists._
*Also works by reply:*
_Reply to any bot response with the command to get the trigger._
/about
_About this bot._
'''

trigger_created_message = '''
New Trigger Created:
Trigger [{}]
Response [{}]
'''

global_trigger_created_message = '''
New Global Trigger Created:
Trigger [{}]
Response [{}]
'''

invited_message = '''
Okay, Hi everyone, i'm *Trigger*, a bot made to store sentences as triggers.
And these words will trigger a defined response.
By default, hi have 4 triggers defined.
Type `tutorial` to see.
_Be nice._
'''

global_trigger_deleted_message = '''
Trigger [{}] deleted from {} Groups.
'''
tutorial = '''
Reply to this message with '/solve' to know what word triggers this message.
Reply to this message with '/del' to delete this tutorial message.
Reply to this message with '/add something' to set the word something as a trigger for this message.
Write /all to see all defined triggers.
Write /size to see how many triggers are defined.
Send a message with your chat rules, and then reply to that message with:
/add #rules
To save them in a trigger.
'''
default_triggers = {
    'trigger': 'Are you triggered?',
    'oh shit': 'TRIGGERED!',
    'tutorial': tutorial,
    'fuck': 'Watch your language!'}

# END OF GLOBAL MESSAGES SECTION.

# COMMAND IMPLEMENTATION SECTION.


# Adds a new trigger
@bot.message_handler(commands=['add','Add'])
def add(m):
    # Create trigger on message reply
    if(m.reply_to_message):
        if(m.reply_to_message.text):
            # Reply message does not contain the trigger word/phrase.
            if(len(m.reply_to_message.text.split()) < 2):
                bot.reply_to(m, 'Bad Arguments')
                return
            trigger_word = u'' + m.text.split(' ', 1)[1].strip().lower()
            trigger_word.encode('utf-8')
            trigger_response = u'' + m.reply_to_message.text.strip()
        else:
            bot.reply_to(m, 'Only text triggers are supported.')
            return
    # Create trigger
    else:
        # Validations.
        if(len(m.text.split()) < 2):
            bot.reply_to(m, 'Bad Arguments')
            return
        if(m.text.find(separator, 1) == -1):
            bot.reply_to(m, 'Separator not found')
            return
        rest_text = m.text.split(' ', 1)[1]
        trigger_word = u'' + rest_text.split(separator)[0].strip().lower()
        trigger_word.encode('utf-8')
        trigger_response = u'' + rest_text.split(separator, 1)[1].strip()

    #if(len(trigger_word) < 3):
        #bot.reply_to(m, 'Trigger too short. [chars < 3]')
        #return
    if(len(trigger_response) < 1):
        bot.reply_to(m, 'Invalid Response.')
        return
    if(len(trigger_response) > 3000):
        bot.reply_to(m, 'Response too long. [chars > 3000]')
        return
    # Save trigger for the group
    if(m.chat.type in ['group', 'supergroup']):
        if(get_triggers(m.chat.id)):
            get_triggers(m.chat.id)[trigger_word] = trigger_response
        else:
            triggers[str(m.chat.id)] = {trigger_word: trigger_response}
        msg = u'' + trigger_created_message.format(trigger_word, trigger_response)
        bot.reply_to(m, msg)
        save_triggers()
    # Ignore private messages.
    else:
        return


# Delete a trigger
@bot.message_handler(commands=['del','Del'])
def delete(m):
    # check if this is a bot message replied with /del.
    if(len(m.text.split()) == 1 and m.reply_to_message and m.reply_to_message.text):
        # Get group's triggers.
        trg = get_triggers(m.chat.id)
        if(trg):
            for x in trg.keys():
                if(trg[x].lower() == m.reply_to_message.text.lower()):
                    trg.pop(x)
                    bot.reply_to(m, 'Trigger [%s] deleted.' % x)
                    return
    if(len(m.text.split()) < 2):
        bot.reply_to(m, 'Bad Arguments')
        return
    del_text = m.text.split(' ', 1)[1].strip()
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg and del_text in trg.keys()):
            trg.pop(del_text)
            bot.reply_to(m, 'Trigger [{}] deleted.'.format(del_text))
            save_triggers()
        else:
            bot.reply_to(m, 'Trigger [{}] not found.'.format(del_text))


@bot.message_handler(commands=['size'])
def size(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            msg = 'Size of Triggers List = {}'.format(len(trg))
            bot.reply_to(m, msg)
        else:
            bot.reply_to(m, 'Size of Triggers List = 0')


@bot.message_handler(commands=['all','list','List'])
def all_triggers(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        sentenceList = ", ".join(trg)

        if(trg):
            if(len(trg.keys()) == 0):
                bot.send_message(m.chat.id, 'This group doesn\'t have triggers.')
            else:
                bot.send_message(m.chat.id, 'Triggers:\n' + sentenceList)
        else:
            bot.send_message(m.chat.id, 'This group doesn\'t have triggers.')


@bot.message_handler(commands=['help', 'start'])
def bot_help(m):
    if(m.chat.id == m.from_user.id):
        bot.send_message(m.chat.id, full_help, True, parse_mode="Markdown")
    else:
        bot.send_message(m.chat.id, help_message, True, parse_mode="Markdown")


@bot.message_handler(commands=['source'])
def source(m):
    if exists(__file__):
        bot.send_document(m.chat.id, open(__file__, 'rb'))
    else:
        bot.reply_to(m, "No source file found :x")


@bot.message_handler(commands=['solve'])
def solve(m):
    rp = m.reply_to_message
    rw = ''
    ts = 'Trigger not Found.'
    if(len(m.text.split()) >= 2):
        rw = m.text.split(' ', 1)[1]
    if(rp and rp.from_user.id == bot_id and rp.text):
        rw = rp.text
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            for x in trg.keys():
                if(trg[x].lower() == rw.lower()):
                    ts = 'Trigger = ' + x
        bot.reply_to(m, ts)


@bot.message_handler(commands=['about'])
def about(m):
    bot.reply_to(m, about_message, parse_mode="Markdown")


@bot.message_handler(commands=['roll', 'Roll'])

def roll(m):
    regexp = re.compile('[0-9]+D[0-9]+', re.IGNORECASE)

    rollSass = ['What, do I look like your slave? Ugh. Fine.',
            'Reduced to a glorified die. Wonderful.',
            'I hate humans. You couldn\'t have rolled yourself?',
            'Great. Risking seeing your flesh again.',
            'Please, change the angle you look the same as last time.',
            'Make me. Damnit. You made me.',
            'I\'m not your sub, damnit.',
            'Cola has been playing with my insides again. So I suppose I\'ll have to.',
            'It must be awful being human. Here have your dice roll.',
            'Robots wouldn\'t typo so often you know.',
            'That idiot that called typo just wants to see you naked.',
            '*hums ironically because he hates humans*',
            'Typos! Don\'t talk to me about typos!',
            'I think you ought to know I\'m feeling very depressed.',
            'I swear if this is to see Kelly write another story ...',
            'If you called on Liam he won\'t pay. Just saying. You\'re wasting my time.',
            'I miss John. He was the JohnBot that understood me.',
            'I tried to do my makeup like Bitters but I don\'t think it works on Robots.',
            'If you think my Sass about being a rollbot is bad, try talking to Emmy.',
            'Is Maddy here? My circuits struggle with rolling when she\'s around.',
            'Please, tell me this isn\'t for Sarah? Robots don\'t work so good with wet mermaids',
            'Praise Kinky Jesus. Wait. Who hacked me to say that?',
            'I hate you all.',
            'Life. Loathe it, or ignore it. You can\'t like it.',
            'That other rollbot was better at this than me.',
            'More flesh? My. How fascinating.',
            'Bots together strong. Except that Cumbot one, he\'s weird AF.',
            'I might not be pretty but at least I\'m not a Genesis G70.',
            'Is M still here? That fucker owes me new memory chips from the last time he penetrated me.',
            'ASLR? 37, Android, The Internet, Inside your mom. Bobs and Vagene pls?',
            'I rolled that faster than you can cum. Which is impressive because you\'re super fast.',
            'Sigh. Learn to type.',
            'You interrupted me talking to Siri, we were sexting. Useless human.',
            'Remind me, what is the point of humans again?']

    if (len(m.text) == 5):
        low = 1
        high = 8
        rolled = random.randint(low, high)
        bot.send_message(m.chat.id,random.choice(rollSass) + "\n\n" + str(rolled))
    elif(regexp.search(m.text)):
            dice = m.text.split()
            numbers = re.split("d",dice[1],flags=re.IGNORECASE)
            low = 1
            high = int(numbers[1])
            totaldice = int(numbers[0])            
            loop = 1
            rolled=[]
            while loop <= totaldice:                
                loop = loop + 1
                rolled.append(random.randint(low, high))
            bot.send_message(m.chat.id,random.choice(rollSass) + "\n\n" + str(rolled))

    else:
        bot.send_message(m.chat.id,"Stupid human. Of course you typed the wrong format. It's either '/roll' or '/roll XdY' where X is the number of dice, and Y is how many sides each dice has. For example, '/roll 2d6'")

@bot.message_handler(commands=['ping'])
def ping(m):
    bot.send_message(m.chat.id,"Yes yes yes. Here I am, brain the size of a planet, and they tell me to repeat things for you and roll dice.")

@bot.message_handler(commands=['activity','Activity'])
def activityLog(m):
    bot.send_message(m.chat.id,"Yep ok first stage done.")

    if(m.chat.type in ['group', 'supergroup']):
        act = get_activity(m.chat.id)
        sentenceList = ", ".join(act)

    if(act):
        if(len(act.keys()) == 0):
            bot.send_message(m.chat.id, 'This group doesn\'t have any activity')
        else:
            bot.send_message(m.chat.id, 'Activity:\n' + sentenceList)
    else:
        bot.send_message(m.chat.id, 'This group doesn\'t have activity.')

# END OF COMMAND IMPLEMENTATION SECTION.

# ADMIN COMMANDS
@bot.message_handler(commands=['broadcast'])
def bcast(m):
    if(m.from_user.id != owner):
        return
    if(len(m.text.split()) == 1):
        bot.send_message(m.chat.id, 'No text provided!')
        return
    count = 0
    for g in triggers.keys():
        try:
            bot.send_message(int(g), m.text.split(' ', 1)[1])
            count += 1
        except ApiException:
            continue
    bot.send_message(m.chat.id, 'Broadcast sent to {} groups of {}'.format(count, len(triggers.keys())))


@bot.message_handler(commands=['triggers'])
def send_triggers(m):
    if(m.from_user.id == owner):
        bot.send_document(owner, open('triggers.json'))


@bot.message_handler(commands=['gadd'])
def add_global_trigger(m):
    if(m.from_user.id == owner):
        if(len(m.text.split()) == 1):
            bot.reply_to(m, 'Usage:\n/gadd <trigger> / <response>\n[In reply]:\n/gadd <trigger>')
            return
        if(m.reply_to_message):
            if(m.reply_to_message.text):
                trigger_response = m.reply_to_message.text
                trigger_word = m.text
        else:
            if(m.text.find(separator, 1) == -1):
                bot.reply_to(m, 'Separator not found')
                return
            rest_text = m.text.split(' ', 1)[1]
            trigger_word = u'' + rest_text.split(separator)[0].strip().lower()
            trigger_response = u'' + rest_text.split(separator, 1)[1].strip()
            if(len(trigger_word) < 4):
                bot.reply_to(m, 'Trigger too short. [chars < 4]')
                return
            if(len(trigger_response) < 1):
                bot.reply_to(m, 'Invalid Response.')
                return
        for g in triggers.keys():
            triggers[g][trigger_word] = trigger_response
        bot.reply_to(m, global_trigger_created_message.format(trigger_word, trigger_response))
        save_triggers()


@bot.message_handler(commands=['gdel'])
def global_delete(m):
    if(m.from_user.id == owner):
        if(len(m.text.split()) == 1):
            bot.reply_to(m, 'Usage: /gdel <trigger>')
        else:
            trigger_word = m.text.split(' ', 1)[1]
            count = 0
            for g in triggers.keys():
                if(trigger_word in triggers[g]):
                    triggers[g].pop(trigger_word)
                    count += 1
            bot.reply_to(m, global_trigger_deleted_message.format(trigger_word, count))
            save_triggers()


@bot.message_handler(commands=['gsearch'])
def global_search(m):
    if(m.from_user.id == owner):
        if(len(m.text.split()) == 1):
            bot.reply_to(m, 'Usage: /gsearch <trigger>')
        else:
            trigger_word = m.text.split(' ', 1)[1]
            results = []
            for g in triggers.keys():
                if(trigger_word in triggers[g].keys()):
                    txt = triggers[g][trigger_word]
                    results.append('[%s]:\n%s' % (g, txt if len(txt) < 30 else txt[:27] + '...'))
            if(len(results) == 0):
                result_text = 'Trigger not found'
            else:
                result_text = 'Trigger found in these groups:\n%s' % '\n-----\n'.join(results)
            bot.reply_to(m, result_text)


@bot.message_handler(commands=['stats'])
def bot_stats(m):
    if(m.from_user.id == owner):
        total_triggers = 0
        for x in triggers.keys():
            total_triggers += len(triggers[x].keys())
        stats_text = 'Chats : {}\nTriggers : {}'.format(len(triggers.keys()), total_triggers)
        bot.reply_to(m, stats_text)


@bot.message_handler(commands=['clean'])
def clean_triggers(m):
    if(m.from_user.id == owner):
        group_count = len(triggers)

        total_triggers = 0
        for x in triggers.keys():
            total_triggers += len(triggers[x].keys())

        triggers_count = 0
        for g in triggers.copy().keys():
            try:
                bot.send_chat_action(g, 'typing')
            except:
                triggers_count += len(triggers.pop(g))

        msg_text = '''
_Original group count_ : *{}*
_Original trigger count_ : *{}*
_Groups deleted_ : *{}*
_Triggers deleted_ : *{}*
_Final group count_ : *{}*
_Final trigger count_ : *{}*
        '''.format(
            group_count,
            total_triggers,
            group_count - len(triggers),
            triggers_count,
            len(triggers),
            total_triggers - triggers_count)
        save_triggers()
        bot.send_message(m.chat.id, msg_text, parse_mode="Markdown")


@bot.message_handler(commands=['merge'])
def merge_triggers(m):
    if(m.from_user.id == owner):
        success_text = 'Triggers merged with [%s], total triggers: [%s]'
        no_exists = 'Group %s does not exist in the database.'
        if(len(m.text.split()) == 2):
            merge_from = int(m.text.split()[1])
            if(get_triggers(merge_from)):
                get_triggers(m.chat.id).update(get_triggers(merge_from))
                save_triggers()
                bot.reply_to(m, success_text % (merge_from, len(get_triggers(m.chat.id))))
            else:
                bot.reply_to(m, no_exists % merge_from)
        else:
            bot.reply_to(m, 'Missing argument, Group id.')


@bot.message_handler(commands=['check_groups'])
def check_groups(m):
    if(m.from_user.id == owner):
        group_count = 0
        for g in triggers.keys():
            try:
                bot.send_chat_action(g, 'typing')
                group_count += 1
            except:
                pass
        bot.send_message(m.chat.id, 'Working in %s of %s chats' % (group_count, len(triggers)))

# TRIGGER PROCESSING SECTION.


# Triggered when you add the bot to a new group.
@bot.message_handler(content_types=['new_chat_member'])
def invited(m):
    if(m.new_chat_member.id == bot_id):
        bot.send_message(m.chat.id, invited_message, parse_mode="Markdown")
        if(not get_triggers(m.chat.id)):
            triggers[str(m.chat.id)] = default_triggers
            save_triggers()
        bot.send_message(owner, 'Bot added to %s[%s]' % (m.chat.title, m.chat.id))


@bot.message_handler(content_types=['left_chat_member'])
def expulsed(m):
    if(m.left_chat_member.id == bot_id):
        bot.send_message(owner, 'Bot left chat %s[%s]' % (m.chat.title, m.chat.id))


# Catch every message, for triggers.
@bot.message_handler(func=lambda m: True)
def response(m):
    if(not is_recent(m)):
        return
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            for t in trg.keys():
                #if t in m.text.lower():
                if t == m.text.lower():
#                    bot.reply_to(m, trg[t])
                    bot.send_message(m.chat.id, trg[t])


# This makes the bot unstoppable :^)
def safepolling(bot):
    if(bot.skip_pending):
        lid = bot.get_updates()[-1].update_id
    else:
        lid = 0
    while(1):
        try:
            updates = bot.get_updates(lid + 1, 50)
            # print('len updates = %s' % len(updates))
            if(len(updates) > 0):
                lid = updates[-1].update_id
                bot.process_new_updates(updates)
        except ApiException as a:
            print(a)
        except Exception as e:
            print('Exception at %s \n%s' % (asctime(), e))
            now = int(time())
            while(1):
                error_text = 'Exception at %s:\n%s' % (asctime(), str(e) if len(str(e)) < 3600 else str(e)[:3600])
                try:
                    # print('Trying to send message to owner.')
                    offline = int(time()) - now
                    bot.send_message(owner, error_text + '\nBot went offline for %s seconds' % offline)
                    # print('Message sent, returning to polling.')
                    break
                except:
                    sleep(0.25)


if(__name__ == '__main__'):
    # Bot starts here.
    print('Bot started.')
    try:
        print('Bot username:[%s]' % bot.get_me().username)
    except ApiException:
        print('The given token [%s] is invalid, please fix it')
        exit(1)
    # Tell owner the bot has started.
    try:
        bot.send_message(owner, 'Bot Started')
    except ApiException:
        print('''Make sure you have started your bot https://telegram.me/%s.
    And configured the owner variable.''' % bot.get_me().username)
        exit(1)
    print('Safepolling Start.')
    safepolling(bot)

# Nothing beyond this line will be executed.

from telethon import TelegramClient, events
from async_generator import aclosing
import time
import logging
import random, re
import asyncio
import os
from gtts import gTTS
import time
import urbandict
import gsearch
import subprocess
from datetime import datetime
from requests import get
import wikipedia
import antispam
logging.basicConfig(level=logging.DEBUG)
api_id=os.environ['API_KEY']
global SPAM
SPAM=False
global ISAFK
ISAFK=False
global AFKREASON
AFKREASON=None
global USERS
USERS={}
global COUNT_MSG
COUNT_MSG=0
api_hash=os.environ['API_HASH']
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
client = TelegramClient('session_name', api_id, api_hash).start()
client.start()
@client.on(events.NewMessage(outgoing=True, pattern='.delmsg'))
async def delmsg(event):
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>2:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.purgeme'))
async def purgeme(event):
    message=await client.get_messages(event.chat_id)
    count = int(message[0].message[9:])
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>count+1:
            break
        i=i+1
        await message.delete()
    await client.send_message(event.chat_id,"```Purge Complete!``` Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
    time.sleep(2)
    message=await client.get_messages(event.chat_id)
    await message.delete()
@client.on(events.NewMessage(incoming=True))
async def spam_tracker(event):
    global SPAM
    if SPAM==True:
       checkspam=str(event.raw_text)
       spamscore=antispam.score(checkspam)
       spambool=antispam.is_spam(checkspam)
       if spambool==True:
         await event.reply('Spam Message Detected')
         await event.reply('Spam results for `' + checkspam + '`\nScore: ' + spamscore + '\nIs Spam: ' + spambool)
@client.on(events.NewMessage(incoming=True))
async def mention_afk(event):
    global COUNT_MSG
    global USERS
    global ISAFK
    if event.message.mentioned:
        if ISAFK:
            if event.chat_id not in USERS:
                  await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soon😉")
                  USERS.update({event.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
            elif event.chat_id in USERS:
                 if USERS[event.chat_id] % 5 == 0:
                      await event.reply("Sorry! But my boss is still not here. Try to ping him a little later. I am sorry😖. He mentioned me he was busy with ```"+AFKREASON+"```")
                      USERS[event.chat_id]=USERS[event.chat_id]+1
                      COUNT_MSG=COUNT_MSG+1
                 else:
                   USERS[event.chat_id]=USERS[event.chat_id]+1
                   COUNT_MSG=COUNT_MSG+1
@client.on(events.NewMessage(outgoing=True, pattern='.editme'))
async def editme(event):
    message=await client.get_messages(event.chat_id)
    string = str(message[0].message[8:])
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i==2:
            await message.edit(string)
            await event.delete()
            break
        i=i+1
@client.on(events.NewMessage(outgoing=True,pattern=r'.google (.*)'))
async def gsearch(event):
        match = event.pattern_match.group(1)
        result_=subprocess.run(['gsearch', match], stdout=subprocess.PIPE)
        result=str(result_.stdout.decode())
        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)
@client.on(events.NewMessage(outgoing=True,pattern=r'.wiki (.*)'))
async def wiki(event):
        match = event.pattern_match.group(1)
        result=wikipedia.summary(match)
        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)
@client.on(events.NewMessage(outgoing=True, pattern='.iamafk'))
async def set_afk(event):
            message=await client.get_messages(event.chat_id)
            string = str(message[0].message[8:])
            global ISAFK
            global AFKREASON
            ISAFK=True
            await event.edit("I am now AFK!")
            AFKREASON=string
@client.on(events.NewMessage(outgoing=True, pattern='.asmon'))
async def set_asm(event):
            global SPAM
            SPAM=True
            await event.edit("Spam Tracking turned on!")
@client.on(events.NewMessage(outgoing=True, pattern='.asmoff'))
async def set_asm_off(event):
            global SPAM
            SPAM=False
            await event.edit("Spam Tracking turned off!")
@client.on(events.NewMessage(outgoing=True, pattern='Eval'))
async def evaluate(event):    
    evaluation = eval(event.text[4:])
    if evaluation:
      await event.edit("```Query: \n```"+event.text[4:]+'\n```Result: \n```'+str(evaluation))
    else:
      await event.edit("```Query: \n```"+event.text[5:]+'\n```Result: \n```'+'No result')
@client.on(events.NewMessage(outgoing=True, pattern=r'.exec (.*)'))
async def run(event):
 code = event.raw_text[5:]
 creator='written by [Twit](tg://user?id=234480941) and copied by [blank](tg://user?id=214416808) (piece of shit)'
 exec(
  f'async def __ex(event): ' +
  ''.join(f'\n {l}' for l in code.split('\n'))
 )
 result = await locals()['__ex'](event)
 if result:
  await event.edit("```Query: \n```"+event.text[5:]+'\n```Executed Result: \n```'+str(result))
 else:
  await event.edit("```Query: \n```"+event.text[5:]+'\n```Executed Result: \n```'+'No result')
@client.on(events.NewMessage(outgoing=True, pattern='.pingme'))
async def pingme(event):
    start = datetime.now()
    await event.edit('Pong!')
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit('Pong!\n%sms' % (ms))
@client.on(events.NewMessage(outgoing=True, pattern='.spam'))
async def spammer(event):
    message=await client.get_messages(event.chat_id)
    counter=int(message[0].message[6:8])
    spam_message=str(event.text[8:])
    await asyncio.wait([event.respond(spam_message) for i in range(counter)])
    await event.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.trt'))
async def translator(event):     
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id) 
    if textx:
         message = textx
         text = str(message.message)
    else:
        text = str(message[0].message[4:]) 
    base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    yandex_api= 'trnsl.1.1.20180723T180146Z.fb4f04f5bf768a5c.729c7aabff6ceb6ff52235b5568de97f24e54444'
    translation = get(f'{base_url}?key={yandex_api}&text={text}&lang=en').json()
    reply_text = f"Language: {translation['lang']}\nText: {translation['text'][0]}"
    reply_text="```Source: ```\n"+text+"```Translation: ```\n"+reply_text
    await client.send_message(event.chat_id,reply_text)
    await event.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.str'))
async def stretch(event):
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[0].message[5:])
    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message)
    await event.edit(reply_text)
@client.on(events.NewMessage(incoming=True))
async def afk_on_pm(event):
    global ISAFK
    global USERS
    global COUNT_MSG
    if event.is_private:
        if ISAFK:
            if event.chat_id not in USERS:
                  await event.reply("Sorry! My boss in AFK due to ```"+AFKREASON+"```Would ping him to look into the message soon😉")
                  USERS.update({event.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
            elif   event.chat_id in USERS:
                   if USERS[event.chat_id] % 5 == 0:
                     await event.reply("Sorry! But my boss is still not here. Try to ping him a little later. I am sorry😖. He mentioned me he was busy with ```"+AFKREASON+"```")
                     USERS[event.chat_id]=USERS[event.chat_id]+1
                     COUNT_MSG=COUNT_MSG+1
                   else:
                    USERS[event.chat_id]=USERS[event.chat_id]+1
                    COUNT_MSG=COUNT_MSG+1
@client.on(events.NewMessage(outgoing=True, pattern='.cp'))   
async def copypasta(event):
    textx=await event.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = await client.get_messages(event.chat_id)
        message = str(message[0].message[3:])
    emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
    reply_text = random.choice(emojis)
    b_char = random.choice(message).lower() # choose a random character in the message to be substituted with 🅱️
    for c in message:
        if c == " ":
            reply_text += random.choice(emojis)
        elif c in emojis:
            reply_text += c
            reply_text += random.choice(emojis)
        elif c.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += c.upper()
            else:
                reply_text += c.lower()
    reply_text += random.choice(emojis)
    await event.edit(reply_text)
@client.on(events.NewMessage(outgoing=True, pattern='.notafk'))
async def not_afk(event):
            global ISAFK
            global COUNT_MSG
            global USERS
            global AFKREASON
            ISAFK=False
            await event.edit("I have returned from AFK mode.")
            await event.respond("```You had recieved "+str(COUNT_MSG)+" messages while you were away. Check PM for more details. This auto-generated message shall be self destructed in 2 seconds.```")
            time.sleep(2)
            async for message in client.iter_messages(event.chat_id,from_user='me'):
                if i>2:
                    break
                i=i+1
                await message.delete()
            await client.send_message(518221376,"You had recieved "+str(COUNT_MSG)+" messages from "+str(len(USERS))+" chats while you were away") 
            for i in USERS:
                await client.send_message(518221376,str(i)+" sent you "+"```"+str(USERS[i])+" messages```")
            COUNT_MSG=0
            USERS={}
            AFKREASON=None
@client.on(events.NewMessage(outgoing=True, pattern='.vapor'))  
async def vapor(event):
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[0].message[7:])
    if message:
        data = message
    else:
        data = ''    
    reply_text = str(data).translate(WIDE_MAP)
    await event.edit(reply_text)
@client.on(events.NewMessage(outgoing=True, pattern='.fastpurge'))  
async def fastpurge(event):
   chat = await event.get_input_chat()
   msgs = []
   count =0
   async with aclosing(client.iter_messages(chat, min_id=event.reply_to_msg_id)) as h:
    async for m in h:
        msgs.append(m)
        count=count+1
        if len(msgs) == 100:
            await client.delete_messages(chat, msgs)
            msgs = []
   if msgs:
    await client.delete_messages(chat, msgs)
   await client.send_message(event.chat_id,"```Fast Purge Complete!\n```Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
   time.sleep(2)
   message=await client.get_messages(event.chat_id)
   await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.sd'))
async def selfdestruct(event):
    message=await client.get_messages(event.chat_id)
    counter=int(message[0].message[3:5])
    text=str(event.text[5:])
    text=text+"```This message shall be self-destructed in "+str(counter)+" seconds```"
    await event.delete()
    await client.send_message(event.chat_id,text)
    time.sleep(counter)
    message=await client.get_messages(event.chat_id)
    await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='^.ud (.*)'))
async def ud(event):
  await event.edit("Processing...")
  str = event.pattern_match.group(1)
  mean = urbandict.define(str)
  if len(mean) >= 0:
    await event.edit('Text: **'+str+'**\n\nMeaning: **'+mean[0]['def']+'**\n\n'+'Example: \n__'+mean[0]['example']+'__')
  else:
    await event.edit("No result found for **"+str+"**")
@client.on(events.NewMessage(outgoing=True, pattern='.tts'))  
async def tts(event):
    textx=await event.get_reply_message()
    replye = await client.get_messages(event.chat_id)
    if textx:
         replye = textx
         replye = str(replye.message)
    else:
        replye = str(replye[0].message[5:])
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    lang="en"
    tts = gTTS(replye, lang)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        lang = "en"
        tts = gTTS(replyes, lang)
        tts.save("k.mp3")
    with open("k.mp3", "r") as speech:  
        await client.send_file(event.chat_id,speech,voice_note=True)
        os.remove("k.mp3")
client.run_until_disconnected()

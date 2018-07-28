from telethon import TelegramClient, events
from async_generator import aclosing
import time
import logging
import random, re
import asyncio
from async_generator import aclosing
import pytest
from datetime import datetime
import os
from requests import get
logging.basicConfig(level=logging.DEBUG)
api_id=os.environ['API_KEY']
global ISAFK
ISAFK=False
api_hash=os.environ['API_HASH']
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
client = TelegramClient('session_name', api_id, api_hash).start()
client.start()
@client.on(events.NewMessage(outgoing=True, pattern='/delmsg'))
async def delmsg(event):
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>2:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='/purgeme'))
async def purgeme(event):
    message=await client.get_messages(event.chat_id)
    count = int(message[0].message[9:])
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>count+1:
            break
        i=i+1
        await message.delete()
    await client.send_message(event.chat_id,"```Purge Complete!``` Purged "+str(count)+" messages.")
@client.on(events.NewMessage(incoming=True))
async def mention_afk(event):
    if event.message.mentioned:
        if ISAFK:
            await event.reply('Sorry! I am currently AFK! Will look into the message as soon as I return😉')
@client.on(events.NewMessage(outgoing=True, pattern='/editme'))
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
@client.on(events.NewMessage(outgoing=True, pattern='/iamafk'))
async def set_afk(event):
            global ISAFK
            ISAFK=True
            await event.edit("I am now AFK!")
@client.on(events.NewMessage(outgoing=True, pattern='Eval'))
async def evaluate(event):    
    evaluation = eval(event.text[4:])
    await event.edit("```Query: \n```"+event.text[4:]+'\n```Result: \n```'+str(evaluation))
@client.on(events.NewMessage(outgoing=True, pattern=r'/exec pycmd (.*)'))
async def run(event):
 code = event.raw_text[12:]
 creator='written by [Twit](tg://user?id=234480941) and copied by [blank](tg://user?id=214416808) (piece of shit)'
 exec(
  f'async def __ex(event): ' +
  ''.join(f'\n {l}' for l in code.split('\n'))
 )
 result = await locals()['__ex'](event)
 if result:
  await event.reply(str(result))
@client.on(events.NewMessage(outgoing=True, pattern='/pingme'))
async def pingme(event):
    start = datetime.now()
    await event.edit('Pong!')
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit('Pong!\n%sms' % (ms))
@client.on(events.NewMessage(outgoing=True, pattern='/spam'))
async def spammer(event):
    message=await client.get_messages(event.chat_id)
    counter=int(message[0].message[6:8])
    spam_message=str(event.text[8:])
    await asyncio.wait([event.respond(spam_message) for i in range(counter)])
    await event.delete()
@client.on(events.NewMessage(outgoing=True, pattern='/translator'))
async def translator(event):     
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id) 
    if textx:
         message = textx
         text = str(message.message)
    else:
        text = str(message[0].message[13:]) 
    base_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    yandex_api= 'trnsl.1.1.20180723T180146Z.fb4f04f5bf768a5c.729c7aabff6ceb6ff52235b5568de97f24e54444'
    translation = get(f'{base_url}?key={yandex_api}&text={text}&lang=en').json()
    reply_text = f"Language: {translation['lang']}\nText: {translation['text'][0]}"
    reply_text="```Source: ```\n"+text+"```Translation: ```\n"+reply_text
    await client.send_message(event.chat_id,reply_text)
    await event.delete()
@client.on(events.NewMessage(outgoing=True, pattern='/stretch'))
async def stretch(event):
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         message = str(message.message)
    else:
        
        message = str(message[0].message[8:])
    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message)
    await event.edit(reply_text)
@client.on(events.NewMessage(incoming=True))
async def afk_on_pm(event):
    if event.is_private:
        if ISAFK:
            await event.reply("Sorry! But I am currently AFK! Would look into the message soon😉")
@client.on(events.NewMessage(outgoing=True, pattern='/copypasta'))   
async def copypasta(event):
    textx=await event.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = await client.get_messages(event.chat_id)
        message = str(message[0].message[10:])
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
@client.on(events.NewMessage(outgoing=True, pattern='/notafk'))
async def not_afk(event):
            global ISAFK
            ISAFK=False
            await event.edit("Hi Guys! I am back!")
@client.on(events.NewMessage(outgoing=True, pattern='/vapor'))  
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
@client.on(events.NewMessage(outgoing=True, pattern='/fastpurge'))  
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
   await client.send_message(event.chat_id,"```Fast Purge Complete!\n```Purged "+str(count)+" messages.")
client.run_until_disconnected()
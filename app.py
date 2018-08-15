
# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from async_generator import aclosing
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from telethon.errors import UserAdminInvalidError
from telethon.errors import ChatAdminRequiredError
from telethon.errors import ChannelInvalidError
from datetime import datetime, timedelta
import time
import logging
import random, re
import asyncio
import os
from gtts import gTTS
import time
import hastebin
import sys
import urbandict
import gsearch
import subprocess
from datetime import datetime
from requests import get
import wikipedia
import inspect
import platform
from googletrans import Translator
from random import randint
from zalgo_text import zalgo
logging.basicConfig(level=logging.DEBUG)
api_id=os.environ['API_KEY']
api_hash=os.environ['API_HASH']
global SPAM
SPAM=False
global ISAFK
ISAFK=False
global AFKREASON
AFKREASON="No Reason"
global USERS
USERS={}
global COUNT_MSG
global SPAM_ALLOWANCE
SPAM_ALLOWANCE=3
global MUTING_USERS
MUTING_USERS={}
COUNT_MSG=0
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
@client.on(events.NewMessage(outgoing=True, pattern='.log'))
async def log(event):
    textx=await event.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = await client.get_messages(event.chat_id)
        message = str(message[0].message[4:])
    await client.send_message(-1001200493978,message)
    await event.edit("`Logged Successfully`")
@client.on(events.NewMessage(outgoing=True, pattern='.term'))
async def terminal_runner(event):
    message=await client.get_messages(event.chat_id)
    command = str(message[0].message)
    list_x=command.split(' ')
    result=subprocess.run(list_x[1:], stdout=subprocess.PIPE)
    result=str(result.stdout.decode())
    await event.edit("**Query: **\n`"+str(command[6:])+'`\n**Output: **\n`'+result+'`')
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
    await client.send_message(event.chat_id,"`Purge Complete!` Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
    await client.send_message(-1001200493978,"Purge of "+str(count)+" messages done successfully.")
    time.sleep(2)
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(incoming=True))
async def spam_tracker(event):
    global SPAM
    global MUTING_USERS
    global SPAM_ALLOWANCE
    if SPAM:
        if event.sender_id not in MUTING_USERS:
                  MUTING_USERS={}
                  MUTING_USERS.update({event.sender_id:1})
        if event.sender_id in MUTING_USERS:
                     MUTING_USERS[event.sender_id]=MUTING_USERS[event.sender_id]+1
                     if MUTING_USERS[event.sender_id]>SPAM_ALLOWANCE:
                         rights = ChannelBannedRights(
                         until_date=datetime.now() + timedelta(days=2),
                         send_messages=True,
                         send_media=True,
                         send_stickers=True,
                         send_gifs=True,
                         send_games=True,
                         send_inline=True,
                         embed_links=True
                         )
                         if event.chat_id > 0:
                             await client.send_message(event.chat_id,"`Boss! I am not trained to deal with people spamming on PM.\n I request to take action with **Report Spam** button`")
                             return
                         try:
                           await client(EditBannedRequest(event.chat_id,event.sender_id,rights))
                         except UserAdminInvalidError:
                           await client.send_message(event.chat_id,"`I'll catch you soon spammer! Now you escaped. `")
                           return
                         except ChatAdminRequiredError:
                           await client.send_message(event.chat_id,"`Boss! You aren't an admin to catch that spammer`")
                           return
                         except ChannelInvalidError:
                           await client.send_message(event.chat_id,"`Boss! I am not trained to deal with people spamming on PM.\n I request to take action with` **Report Spam** `button`")
                           return
                         await client.send_message(event.chat_id,"`Anti-Flood to the rescue! Spammer "+str(event.sender_id)+" was muted.`")
@client.on(events.NewMessage(outgoing=True,pattern='.shg'))
async def shrug(event):
    await event.edit("¯\_(ツ)_/¯")
@client.on(events.NewMessage(outgoing=True,pattern='hi'))
async def hoi(event):
    await event.edit("Hoi!😄")
@client.on(events.NewMessage(outgoing=True,pattern='/get userbotfile'))
async def userbot_sender(event):
    file=open(sys.argv[0], 'r')
    await client.send_file(event.chat_id, sys.argv[0], reply_to=event.id, caption='`Here\'s me in a file`')
    file.close()
@client.on(events.NewMessage(pattern='.pip (.+)'))
async def pipcheck(event):
	a=await event.reply('`Searching . . .`')
	r='`' + subprocess.run(['pip3', 'search', e.pattern_match.group(1)], stdout=subprocess.PIPE).stdout.decode() + '`'
	await a.edit(r)
@client.on(events.NewMessage(outgoing=True,pattern='.paste'))
async def haste_paste(event):
    message=await client.get_messages(event.chat_id)
    await event.reply('`Sending to bin . . .`')
    text=str(message[0].message[7:])
    await event.edit('`Sent to bin! Check it here: `' + hastebin.post(text))
@client.on(events.NewMessage(pattern='.killme'))
async def killmelol(event):
    name = await client.get_entity(event.from_id)
    name0 = str(name.first_name)
    await event.reply('**K I L L  **[' + name0 + '](tg://user?id=' + str(event.from_id) + ')**\n\nP L E A S E\n\nE N D  T H E I R  S U F F E R I N G**')
@client.on(events.NewMessage(outgoing=True,pattern='.rekt'))
async def rekt(event):
    await event.edit("Get Rekt man! ( ͡° ͜ʖ ͡°)")
@client.on(events.NewMessage(outgoing=True,pattern='.thanos'))
async def thanos_to_rescue(event):
    rights = ChannelBannedRights(
                         until_date=None,
                         view_messages=True,
                         send_messages=True,
                         send_media=True,
                         send_stickers=True,
                         send_gifs=True,
                         send_games=True,
                         send_inline=True,
                         embed_links=True
                         )
    await event.edit("`Thanos snaps!`")
    time.sleep(5)
    await client(EditBannedRequest(event.chat_id,(await event.get_reply_message()).sender_id,rights))
    await event.edit("When I’m done, half of humanity will still exist. Perfectly balanced, as all things should be. I hope they remember you.")
@client.on(events.NewMessage(incoming=True))
async def mention_afk(event):
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFKREASON
    if event.message.mentioned:
        if ISAFK:
            if (await event.get_sender()):
              if (await event.get_sender()).username not in USERS:
                  USERS.update({(await event.get_sender()).username:1})
                  COUNT_MSG=COUNT_MSG+1
                  await event.reply("Sorry! My boss in AFK due to `"+AFKREASON+"`Would ping him to look into the message soon😉.Meanwhile you can play around with his AI. **This message shall be self destructed in 5 seconds**")
                  time.sleep(5)
                  i=1
                  async for message in client.iter_messages(event.chat_id,from_user='me'):
                    if i>1:
                        break
                    i=i+1
                    await message.delete()
              elif (await event.get_sender()).username in USERS:
                     USERS[(await event.get_sender()).username]=USERS[(await event.get_sender()).username]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await event.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await event.reply("Bot is off. Better version of it, should be up soon!")
            else:
                  USERS.update({event.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
                  await event.reply("Sorry! My boss in AFK due to `"+AFKREASON+"`Would ping him to look into the message soon😉. Meanwhile you can play around with his AI. **This message shall be self destructed in 5 seconds**")
                  time.sleep(5)
                  i=1
                  async for message in client.iter_messages(event.chat_id,from_user='me'):
                        if i>1:
                           break
                        i=i+1
                        await message.delete()
                  if event.chat_id in USERS:
                     USERS[event.chat_id]=USERS[event.chat_id]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await event.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await event.reply("Bot is down now! A better version of it must be up soon!")
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
    await client.send_message(-1001200493978,"Edit query was executed successfully")
@client.on(events.NewMessage(outgoing=True,pattern=r'.google (.*)'))
async def gsearch(event):
        match = event.pattern_match.group(1)
        result_=subprocess.run(['gsearch', match], stdout=subprocess.PIPE)
        result=str(result_.stdout.decode())
        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)
        await client.send_message(-1001200493978,"Google Search query "+match+" was executed successfully")
@client.on(events.NewMessage(outgoing=True,pattern=r'.wiki (.*)'))
async def wiki(event):
        match = event.pattern_match.group(1)
        result=wikipedia.summary(match)
        await client.send_message(await client.get_input_entity(event.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=event.id, link_preview=False)
        await client.send_message(-1001200493978,"Wiki query "+match+" was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern='.iamafk'))
async def set_afk(event):
            message=await client.get_messages(event.chat_id)
            string = str(message[0].message[8:])
            global ISAFK
            global AFKREASON
            ISAFK=True
            await event.edit("I am now AFK!")
            if string!="":
                AFKREASON=string
@client.on(events.NewMessage(outgoing=True, pattern='.zal'))
async def zal(event):
     textx=await event.get_reply_message()
     message = await client.get_messages(event.chat_id)
     if textx:
         message = textx
         message = str(message.message)
     else:
        message = str(message[0].message[4:])
     input_text = " ".join(message).lower()
     zalgofied_text = zalgo.zalgo().zalgofy(input_text)
     await event.edit(zalgofied_text)
@client.on(events.NewMessage(outgoing=True, pattern='.asmon'))
async def set_asm(event):
            global SPAM
            global SPAM_ALLOWANCE
            SPAM=True
            message=await client.get_messages(event.chat_id)
            SPAM_ALLOWANCE=int(message[0].message[6:])
            await event.edit("Spam Tracking turned on!")
@client.on(events.NewMessage(outgoing=True, pattern='.asmoff'))
async def set_asm_off(event):
            global SPAM
            SPAM=False
            await event.edit("Spam Tracking turned off!")
@client.on(events.NewMessage(outgoing=True, pattern='.eval'))
async def evaluate(event):
    evaluation = eval(event.text[6:])
    if inspect.isawaitable(evaluation):
       evaluation = await evaluation
    if evaluation:
      await event.edit("**Query: **\n`"+event.text[6:]+'`\n**Result: **\n`'+str(evaluation)+'`')
    else:
      await event.edit("**Query: **\n`"+event.text[6:]+'`\n**Result: **\n`No Result Returned/False`')
    await client.send_message(-1001200493978,"Eval query "+event.text[6:]+" was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern=r'.exec (.*)'))
async def run(event):
 code = event.raw_text[5:]
 exec(
  f'async def __ex(event): ' +
  ''.join(f'\n {l}' for l in code.split('\n'))
 )
 result = await locals()['__ex'](event)
 if result:
  await event.edit("**Query: **\n`"+event.text[5:]+'`\n**Result: **\n`'+str(result)+'`')
 else:
  await event.edit("**Query: **\n`"+event.text[5:]+'`\n**Result: **\n`'+'No Result Returned/False'+'`')
 await client.send_message(-1001200493978,"Exec query "+event.text[5:]+" was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern='.pingme'))
async def pingme(event):
    start = datetime.now()
    await event.edit('Pong!')
    end = datetime.now()
    ms = (end - start).microseconds/1000
    await event.edit('Pong!\n%sms' % (ms))
@client.on(events.NewMessage(outgoing=True, pattern='.spam'))
async def spammer(event):
    message= await client.get_messages(event.chat_id)
    counter=int(message[0].message[6:8])
    spam_message=str(event.text[8:])
    await asyncio.wait([event.respond(spam_message) for i in range(counter)])
    await event.delete()
    await client.send_message(-1001200493978,"Spam was executed successfully")
@client.on(events.NewMessage(outgoing=True,pattern='.shutdown'))
async def killdabot(event):
        message=message = await client.get_messages(event.chat_id)
        counter=int(message[0].message[10:])
        await event.reply('`Sorry for the mistakes i did master....`')
        time.sleep(2)
        await event.edit('`Sir i am dead. Cant respond to any commands for sometime`')
        time.sleep(counter)
@client.on(events.NewMessage(outgoing=True, pattern='.help'))
async def help(event):
    await event.reply('https://github.com/baalajimaestro/Telegram-UserBot/blob/master/README.md')
@client.on(events.NewMessage(outgoing=True, pattern='.bigspam'))
async def bigspam(event):
    message = await client.get_messages(event.chat_id)
    counter=int(message[0].message[9:13])
    spam_message=str(event.text[13:])
    for i in range (1,counter):
       await event.respond(spam_message)
    await event.delete()
    await client.send_message(-1001200493978,"bigspam was executed successfully")
@client.on(events.NewMessage(outgoing=True, pattern='.speed'))
async def speedtest(event):
    l=await event.reply('`Running speed test . . .`')
    k=subprocess.run(['speedtest-cli'], stdout=subprocess.PIPE)
    await l.edit('`' + k.stdout.decode()[:-1] + '`')
    await event.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.trt'))
async def translateme(event):
    translator=Translator()
    textx=await event.get_reply_message()
    message = await client.get_messages(event.chat_id)
    if textx:
         message = textx
         text = str(message.message)
    else:
        text = str(message[0].message[4:])
    reply_text=translator.translate(text, dest='en').text
    reply_text="`Source: `\n"+text+"`Translation: `\n"+reply_text
    await client.send_message(event.chat_id,reply_text)
    await event.delete()
    await client.send_message(-1001200493978,"Translate query "+message+" was executed successfully")
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
    global AFKREASON
    if event.is_private:
        if ISAFK:
            if (await event.get_sender()):
              if (await event.get_sender()).username not in USERS:
                  USERS.update({(await event.get_sender()).username:1})
                  COUNT_MSG=COUNT_MSG+1
                  await event.reply("Sorry! My boss in AFK due to `"+AFKREASON+"`Would ping him to look into the message soon😉.  Meanwhile you can play around with his AI.**This message shall be self destructed in 5 seconds**")
                  time.sleep(5)
                  i=1
                  async for message in client.iter_messages(event.chat_id,from_user='me'):
                    if i>1:
                        break
                    i=i+1
                    await message.delete()
              elif (await event.get_sender()).username in USERS:
                     USERS[(await event.get_sender()).username]=USERS[(await event.get_sender()).username]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await event.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await event.reply("Bot is down. A better version of it, must be up now!")
            else:
                  USERS.update({event.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
                  await event.reply("Sorry! My boss in AFK due to `"+AFKREASON+"`Would ping him to look into the message soon😉.  Meanwhile you can play around with his AI. **This message shall be self destructed in 5 seconds**")
                  time.sleep(5)
                  i=1
                  async for message in client.iter_messages(event.chat_id,from_user='me'):
                        if i>1:
                           break
                        i=i+1
                        await message.delete()
                  if event.chat_id in USERS:
                     USERS[event.chat_id]=USERS[event.chat_id]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await event.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await event.reply("Bot is down! A better version of it, must be up now!")
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
            await event.respond("`You had recieved "+str(COUNT_MSG)+" messages while you were away. Check log for more details. This auto-generated message shall be self destructed in 2 seconds.`")
            time.sleep(2)
            i=1
            async for message in client.iter_messages(event.chat_id,from_user='me'):
                if i>1:
                    break
                i=i+1
                await message.delete()
            await client.send_message(-1001200493978,"You had recieved "+str(COUNT_MSG)+" messages from "+str(len(USERS))+" chats while you were away")
            for i in USERS:
                await client.send_message(-1001200493978,str(i)+" sent you "+"`"+str(USERS[i])+" messages`")
            COUNT_MSG=0
            USERS={}
            AFKREASON="No reason"
@client.on(events.NewMessage(outgoing=True, pattern='.runs'))
async def react(event):
    reactor=['Runs to Modi for Help','Runs to Donald Trumpet for help','Runs to Kaala','Runs to Thanos','Runs far, far away from earth','Running faster than usian bolt coz I\'mma Bot','Runs to Marie']
    index=randint(0,len(reactor)-1)
    reply_text=reactor[index]
    await event.edit(reply_text)
    await client.send_message(-1001200493978,"You ran away from a cancerous chat")
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
@client.on(events.NewMessage(outgoing=True, pattern=':/'))
async def dopedance(event):
    uio=['/','\\']
    for i in range (1,15):
        time.sleep(0.3)
        await event.edit(':'+uio[i%2])
@client.on(events.NewMessage(outgoing=True, pattern='-_-'))
async def mutemeow(event):
    await event.delete()
    t = '-_-'
    r = await event.reply(t)
    for j in range(10):
        t = t[:-1] + '_-'
        await r.edit(t)
@client.on(events.NewMessage(outgoing=True, pattern='.react'))
async def react(event):
    reactor=['ʘ‿ʘ','ヾ(-_- )ゞ','(っ˘ڡ˘ς)','(´ж｀ς)','( ಠ ʖ̯ ಠ)','(° ͜ʖ͡°)╭∩╮','(ᵟຶ︵ ᵟຶ)','(งツ)ว','ʚ(•｀','(っ▀¯▀)つ','(◠﹏◠)','( ͡ಠ ʖ̯ ͡ಠ)','( ఠ ͟ʖ ఠ)','(∩｀-´)⊃━☆ﾟ.*･｡ﾟ','(⊃｡•́‿•̀｡)⊃','(._.)','{•̃_•̃}','(ᵔᴥᵔ)','♨_♨','⥀.⥀','ح˚௰˚づ ','(҂◡_◡)','ƪ(ړײ)‎ƪ​​','(っ•́｡•́)♪♬','◖ᵔᴥᵔ◗ ♪ ♫ ','(☞ﾟヮﾟ)☞','[¬º-°]¬','(Ծ‸ Ծ)','(•̀ᴗ•́)و ̑̑','ヾ(´〇`)ﾉ♪♪♪','(ง\'̀-\'́)ง','ლ(•́•́ლ)','ʕ •́؈•̀ ₎','♪♪ ヽ(ˇ∀ˇ )ゞ','щ（ﾟДﾟщ）','( ˇ෴ˇ )','눈_눈','(๑•́ ₃ •̀๑) ','( ˘ ³˘)♥ ','ԅ(≖‿≖ԅ)','♥‿♥','◔_◔','⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾','乁( ◔ ౪◔)「      ┑(￣Д ￣)┍','( ఠൠఠ )ﾉ','٩(๏_๏)۶','┌(ㆆ㉨ㆆ)ʃ','ఠ_ఠ','(づ｡◕‿‿◕｡)づ','(ノಠ ∩ಠ)ノ彡( \\o°o)\\','“ヽ(´▽｀)ノ”','༼ ༎ຶ ෴ ༎ຶ༽','｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡','(づ￣ ³￣)づ','(⊙.☉)7','ᕕ( ᐛ )ᕗ','t(-_-t)','(ಥ⌣ಥ)','ヽ༼ ಠ益ಠ ༽ﾉ','༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽','ミ●﹏☉ミ','(⊙_◎)','¿ⓧ_ⓧﮌ','ಠ_ಠ','(´･_･`)','ᕦ(ò_óˇ)ᕤ','⊙﹏⊙','(╯°□°）╯︵ ┻━┻','¯\_(⊙︿⊙)_/¯','٩◔̯◔۶','°‿‿°','ᕙ(⇀‸↼‶)ᕗ','⊂(◉‿◉)つ','V•ᴥ•V','q(❂‿❂)p','ಥ_ಥ','ฅ^•ﻌ•^ฅ','ಥ﹏ಥ','（ ^_^）o自自o（^_^ ）','ಠ‿ಠ','ヽ(´▽`)/','ᵒᴥᵒ#','( ͡° ͜ʖ ͡°)','┬─┬﻿ ノ( ゜-゜ノ)','ヽ(´ー｀)ノ','☜(⌒▽⌒)☞','ε=ε=ε=┌(;*´Д`)ﾉ','(╬ ಠ益ಠ)','┬─┬⃰͡ (ᵔᵕᵔ͜ )','┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻','¯\_(ツ)_/¯','ʕᵔᴥᵔʔ','(`･ω･´)','ʕ•ᴥ•ʔ','ლ(｀ー´ლ)','ʕʘ̅͜ʘ̅ʔ','（　ﾟДﾟ）','¯\(°_o)/¯','(｡◕‿◕｡)']
    index=randint(0,len(reactor))
    reply_text=reactor[index]
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
   await client.send_message(event.chat_id,"`Fast Purge Complete!\n`Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
   await client.send_message(-1001200493978,"Purge of "+str(count)+" messages done successfully.")
   time.sleep(2)
   i=1
   async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
@client.on(events.NewMessage(outgoing=True, pattern='.sd'))
async def selfdestruct(event):
    message=await client.get_messages(event.chat_id)
    counter=int(message[0].message[4:6])
    text=str(event.text[6:])
    text=text+"`This message shall be self-destructed in "+str(counter)+" seconds`"
    await event.delete()
    await client.send_message(event.chat_id,text)
    time.sleep(counter)
    i=1
    async for message in client.iter_messages(event.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
        await client.send_message(-1001200493978,"sd query done successfully")
@client.on(events.NewMessage(outgoing=True, pattern='^.ud (.*)'))
async def ud(event):
  await event.edit("Processing...")
  str = event.pattern_match.group(1)
  mean = urbandict.define(str)
  if len(mean) >= 0:
    await event.edit('Text: **'+str+'**\n\nMeaning: **'+mean[0]['def']+'**\n\n'+'Example: \n__'+mean[0]['example']+'__')
    await client.send_message(-1001200493978,"ud query "+str+" executed successfully.")
  else:
    await event.edit("No result found for **"+str+"**")
'''@client.on(events.NewMessage(outgoing=True, pattern='.tts'))
async def tts(event):
    textx=await event.get_reply_message()
    replye = await client.get_messages(event.chat_id)
    if textx:
         replye = textx
         replye = str(replye.message)
    else:
        replye = str(replye[0].message[5:])
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    lang="en"
    tts = gTTS(replye, lang)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        lang = "en"                           COMMENTING OUT COZ NO USE OF THIZ UNTIL IT GETS FIXED
        tts = gTTS(replyes, lang)
        tts.save("k.mp3")
    with open("k.mp3", "r") as speech:
        await client.send_file(event.chat_id,speech,voice_note=True)
        os.remove("k.mp3")
@client.on(events.NewMessage(outgoing=True, pattern='.restart'))'''
async def reboot(event):
    await event.edit("`Thank You master! I am taking a break!`")
    os.execl(sys.executable, sys.executable, *sys.argv)
if len(sys.argv) < 2:
    client.run_until_disconnected()

# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from async_generator import aclosing
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from telethon.errors import UserAdminInvalidError
from telethon.errors import ChatAdminRequiredError
from telethon.errors import ChannelInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChannelAdminRights
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
SUDO_USERS=[518221376,538543304,423070089,234480941]
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
bot = TelegramClient('userbot', api_id, api_hash).start()
bot.start()
@bot.on(events.NewMessage(outgoing=True,pattern='.*'))
@bot.on(events.MessageEdited(outgoing=True))
async def common_outgoing_handler(e):
    find = e.text
    find = str(find[1:])
    if find=="delmsg" :
        i=1
        async for message in bot.iter_messages(e.chat_id,from_user='me'):
            if i>2:
                break
            i=i+1
            await message.delete()
    elif find == "shg":
        await e.edit("¯\_(ツ)_/¯")
    elif find == "get userbotfile":
        file=open(sys.argv[0], 'r')
        await bot.send_file(e.chat_id, sys.argv[0], reply_to=e.id, caption='`Here\'s me in a file`')
        file.close()
    elif find == "thanos":
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
        if (await e.get_reply_message()).sender_id in SUDO_USERS:
            await e.edit("`I am not supposed to ban a sudo user!`")
            return
        await e.edit("`Thanos snaps!`")
        time.sleep(5)
        await bot(EditBannedRequest(e.chat_id,(await e.get_reply_message()).sender_id,rights))
        await e.edit("When I’m done, half of humanity will still exist. Perfectly balanced, as all things should be. I hope they remember you.")
    elif find == "spider":
        rights = ChannelBannedRights(
                             until_date=None,
                             view_messages=None,
                             send_messages=True,
                             send_media=True,
                             send_stickers=True,
                             send_gifs=True,
                             send_games=True,
                             send_inline=True,
                             embed_links=True
                             )
        if (await e.get_reply_message()).sender_id in SUDO_USERS:
            await e.edit("`I am not supposed to mute a sudo user!`")
            return
        await e.edit("`Spiderman nabs him!`")
        time.sleep(5)
        await bot(EditBannedRequest(e.chat_id,(await e.get_reply_message()).sender_id,rights))
        await e.edit("I missed the part, that's my problem.")
    elif find == "editme":
        message=e.text
        string = str(message[8:])
        i=1
        async for message in bot.iter_messages(e.chat_id,from_user='me'):
            if i==2:
                await message.edit(string)
                await e.delete()
                break
            i=i+1
        await bot.send_message(-1001200493978,"Edit query was executed successfully")
    elif find == "wizard":
        rights = ChannelAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        invite_link=True,
        )
        await e.edit("`Wizard waves his wand!`")
        time.sleep(3)
        await bot(EditAdminRequest(e.chat_id,(await e.get_reply_message()).sender_id,rights))
        await e.edit("A perfect magic has happened!")
    elif find == "asmoff":
        global SPAM
        SPAM=False
        await e.edit("Spam Tracking turned off!")
    elif find=="rekt":
        await e.edit("Get Rekt man! ( ͡° ͜ʖ ͡°)")
    elif find=="speed":
            l=await e.reply('`Running speed test . . .`')
            k=subprocess.run(['speedtest-cli'], stdout=subprocess.PIPE)
            await l.edit('`' + k.stdout.decode()[:-1] + '`')
            await e.delete()
    elif find=="notafk":
        global ISAFK
        global COUNT_MSG
        global USERS
        global AFKREASON
        ISAFK=False
        await e.edit("I have returned from AFK mode.")
        await e.respond("`You had recieved "+str(COUNT_MSG)+" messages while you were away. Check log for more details. This auto-generated message shall be self destructed in 2 seconds.`")
        time.sleep(2)
        i=1
        async for message in bot.iter_messages(e.chat_id,from_user='me'):
            if i>1:
                break
            i=i+1
            await message.delete()
        await bot.send_message(-1001200493978,"You had recieved "+str(COUNT_MSG)+" messages from "+str(len(USERS))+" chats while you were away")
        for i in USERS:
            await bot.send_message(-1001200493978,str(i)+" sent you "+"`"+str(USERS[i])+" messages`")
        COUNT_MSG=0
        USERS={}
        AFKREASON="No reason"
    elif find=="runs":
        reactor=['Runs to Modi for Help','Runs to Donald Trumpet for help','Runs to Kaala','Runs to Thanos','Runs far, far away from earth','Running faster than usian bolt coz I\'mma Bot','Runs to Marie']
        index=randint(0,len(reactor)-1)
        reply_text=reactor[index]
        await e.edit(reply_text)
        await bot.send_message(-1001200493978,"You ran away from a cancerous chat")
    elif find==":/":
        uio=['/','\\']
        for i in range (1,15):
            time.sleep(0.3)
            await e.edit(':'+uio[i%2])
    elif find=="-_-":
        await e.delete()
        t = '-_-'
        r = await e.reply(t)
        for j in range(10):
            t = t[:-1] + '_-'
            await r.edit(t)
    elif find=="react":
        reactor=['ʘ‿ʘ','ヾ(-_- )ゞ','(っ˘ڡ˘ς)','(´ж｀ς)','( ಠ ʖ̯ ಠ)','(° ͜ʖ͡°)╭∩╮','(ᵟຶ︵ ᵟຶ)','(งツ)ว','ʚ(•｀','(っ▀¯▀)つ','(◠﹏◠)','( ͡ಠ ʖ̯ ͡ಠ)','( ఠ ͟ʖ ఠ)','(∩｀-´)⊃━☆ﾟ.*･｡ﾟ','(⊃｡•́‿•̀｡)⊃','(._.)','{•̃_•̃}','(ᵔᴥᵔ)','♨_♨','⥀.⥀','ح˚௰˚づ ','(҂◡_◡)','ƪ(ړײ)‎ƪ​​','(っ•́｡•́)♪♬','◖ᵔᴥᵔ◗ ♪ ♫ ','(☞ﾟヮﾟ)☞','[¬º-°]¬','(Ծ‸ Ծ)','(•̀ᴗ•́)و ̑̑','ヾ(´〇`)ﾉ♪♪♪','(ง\'̀-\'́)ง','ლ(•́•́ლ)','ʕ •́؈•̀ ₎','♪♪ ヽ(ˇ∀ˇ )ゞ','щ（ﾟДﾟщ）','( ˇ෴ˇ )','눈_눈','(๑•́ ₃ •̀๑) ','( ˘ ³˘)♥ ','ԅ(≖‿≖ԅ)','♥‿♥','◔_◔','⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾','乁( ◔ ౪◔)「      ┑(￣Д ￣)┍','( ఠൠఠ )ﾉ','٩(๏_๏)۶','┌(ㆆ㉨ㆆ)ʃ','ఠ_ఠ','(づ｡◕‿‿◕｡)づ','(ノಠ ∩ಠ)ノ彡( \\o°o)\\','“ヽ(´▽｀)ノ”','༼ ༎ຶ ෴ ༎ຶ༽','｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡','(づ￣ ³￣)づ','(⊙.☉)7','ᕕ( ᐛ )ᕗ','t(-_-t)','(ಥ⌣ಥ)','ヽ༼ ಠ益ಠ ༽ﾉ','༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽','ミ●﹏☉ミ','(⊙_◎)','¿ⓧ_ⓧﮌ','ಠ_ಠ','(´･_･`)','ᕦ(ò_óˇ)ᕤ','⊙﹏⊙','(╯°□°）╯︵ ┻━┻','¯\_(⊙︿⊙)_/¯','٩◔̯◔۶','°‿‿°','ᕙ(⇀‸↼‶)ᕗ','⊂(◉‿◉)つ','V•ᴥ•V','q(❂‿❂)p','ಥ_ಥ','ฅ^•ﻌ•^ฅ','ಥ﹏ಥ','（ ^_^）o自自o（^_^ ）','ಠ‿ಠ','ヽ(´▽`)/','ᵒᴥᵒ#','( ͡° ͜ʖ ͡°)','┬─┬﻿ ノ( ゜-゜ノ)','ヽ(´ー｀)ノ','☜(⌒▽⌒)☞','ε=ε=ε=┌(;*´Д`)ﾉ','(╬ ಠ益ಠ)','┬─┬⃰͡ (ᵔᵕᵔ͜ )','┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻','¯\_(ツ)_/¯','ʕᵔᴥᵔʔ','(`･ω･´)','ʕ•ᴥ•ʔ','ლ(｀ー´ლ)','ʕʘ̅͜ʘ̅ʔ','（　ﾟДﾟ）','¯\(°_o)/¯','(｡◕‿◕｡)']
        index=randint(0,len(reactor))
        reply_text=reactor[index]
        await e.edit(reply_text)
    elif find == "fastpurge":
        chat = await e.get_input_chat()
        msgs = []
        count =0
        async with aclosing(bot.iter_messages(chat, min_id=e.reply_to_msg_id)) as h:
         async for m in h:
             msgs.append(m)
             count=count+1
             if len(msgs) == 100:
                 await bot.delete_messages(chat, msgs)
                 msgs = []
        if msgs:
         await bot.delete_messages(chat, msgs)
        await bot.send_message(e.chat_id,"`Fast Purge Complete!\n`Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
        await bot.send_message(-1001200493978,"Purge of "+str(count)+" messages done successfully.")
        time.sleep(2)
        i=1
        async for message in bot.iter_messages(e.chat_id,from_user='me'):
             if i>1:
                 break
             i=i+1
             await message.delete()
    elif find == "restart":
        await e.edit("`Thank You master! I am taking a break!`")
        os.execl(sys.executable, sys.executable, *sys.argv)
    elif find == "pingme":
        start = datetime.now()
        await e.edit('Pong!')
        end = datetime.now()
        ms = (end - start).microseconds/1000
        await e.edit('Pong!\n%sms' % (ms))
@bot.on(events.NewMessage(outgoing=True, pattern='.log'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.log'))
async def log(e):
    textx=await e.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = e.text
        message = str(message[4:])
    await bot.send_message(-1001200493978,message)
    await e.edit("`Logged Successfully`")
@bot.on(events.NewMessage(outgoing=True, pattern='.term'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.term'))
async def terminal_runner(e):
    message=e.text
    command = str(message)
    list_x=command.split(' ')
    result=subprocess.run(list_x[1:], stdout=subprocess.PIPE)
    result=str(result.stdout.decode())
    await e.edit("**Query: **\n`"+str(command[6:])+'`\n**Output: **\n`'+result+'`')
@bot.on(events.NewMessage(outgoing=True, pattern='.purgeme'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.purgeme'))
async def purgeme(e):
    message=e.text
    count = int(message[9:])
    i=1
    async for message in bot.iter_messages(e.chat_id,from_user='me'):
        if i>count+1:
            break
        i=i+1
        await message.delete()
    await bot.send_message(e.chat_id,"`Purge Complete!` Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
    await bot.send_message(-1001200493978,"Purge of "+str(count)+" messages done successfully.")
    time.sleep(2)
    i=1
    async for message in bot.iter_messages(e.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def spam_tracker(e):
    global SPAM
    global MUTING_USERS
    global SPAM_ALLOWANCE
    if SPAM:
        if e.sender_id not in MUTING_USERS:
                  MUTING_USERS={}
                  MUTING_USERS.update({e.sender_id:1})
        if e.sender_id in MUTING_USERS:
                     MUTING_USERS[e.sender_id]=MUTING_USERS[e.sender_id]+1
                     if MUTING_USERS[e.sender_id]>SPAM_ALLOWANCE:
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
                         if e.chat_id > 0:
                             await bot.send_message(e.chat_id,"`Boss! I am not trained to deal with people spamming on PM.\n I request to take action with **Report Spam** button`")
                             return
                         try:
                           await bot(EditBannedRequest(e.chat_id,e.sender_id,rights))
                         except UserAdminInvalidError:
                           await bot.send_message(e.chat_id,"`I'll catch you soon spammer! Now you escaped. `")
                           return
                         except ChatAdminRequiredError:
                           await bot.send_message(e.chat_id,"`Me nu admeme to catch spammer nibba`")
                           return
                         except ChannelInvalidError:
                           await bot.send_message(e.chat_id,"`User retarded af ._.`")
                           return
                         await bot.send_message(e.chat_id,"`Get rekt nibba. I am ze anti-spam lord "+str(e.sender_id)+" was muted.`")
@bot.on(events.NewMessage(outgoing=True,pattern='.pip (.+)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.pip (.+)'))
async def pipcheck(e):
	a=await e.reply('`Searching . . .`')
	r='`' + subprocess.run(['pip', 'search', e.pattern_match.group(1)], stdout=subprocess.PIPE).stdout.decode() + '`'
	await a.edit(r)
@bot.on(events.NewMessage(outgoing=True,pattern='.paste'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.paste'))
async def haste_paste(e):
    message=e.text
    await e.edit('`Sending to bin . . .`')
    text=str(message[7:])
    await e.edit('`Sent to bin! Check it here: `' + hastebin.post(text))
@bot.on(events.NewMessage(incoming=True,pattern='.killme'))
async def killmelol(e):
    name = await bot.get_entity(e.from_id)
    name0 = str(name.first_name)
    await e.reply('**K I L L  **[' + name0 + '](tg://user?id=' + str(e.from_id) + ')**\n\nP L E A S E\n\nE N D  T H E I R  S U F F E R I N G**')
@bot.on(events.NewMessage(outgoing=True,pattern="hi"))
@bot.on(events.MessageEdited(outgoing=True,pattern="hi"))
async def hoi(e):
    if e.text=="hi":
     await e.edit("Hoi!😄")
@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def mention_afk(e):
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFKREASON
    if e.message.mentioned:
        if ISAFK:
            if (await e.get_sender()):
              if (await e.get_sender()).username not in USERS:
                  USERS.update({(await e.get_sender()).username:1})
                  COUNT_MSG=COUNT_MSG+1
                  await e.reply("AFK AF `"+AFKREASON+"`Spam me if you want me to notice you")
                  time.sleep(10)
                  i=1
                  async for message in bot.iter_messages(e.chat_id,from_user='me'):
                    if i>1:
                        break
                    i=i+1
                    await message.delete()
              elif (await e.get_sender()).username in USERS:
                     USERS[(await e.get_sender()).username]=USERS[(await e.get_sender()).username]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await e.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await e.reply("Bot is off. Better version of it, should be up soon!")
            else:
                  USERS.update({e.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
                  await e.reply("AFK AF `"+AFKREASON+"`Spam me if you want me to notice you")
                  time.sleep(10)
                  i=1
                  async for message in bot.iter_messages(e.chat_id,from_user='me'):
                        if i>1:
                           break
                        i=i+1
                        await message.delete()
                  if e.chat_id in USERS:
                     USERS[e.chat_id]=USERS[e.chat_id]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await e.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await e.reply("Lmao bot dead")
@bot.on(events.NewMessage(outgoing=True,pattern=r'.google (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern=r'.google (.*)'))
async def gsearch(e):
        match = e.pattern_match.group(1)
        result_=subprocess.run(['gsearch', match], stdout=subprocess.PIPE)
        result=str(result_.stdout.decode())
        await bot.send_message(await bot.get_input_entity(e.chat_id), message='**Search Query:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=e.id, link_preview=False)
        await bot.send_message(-1001200493978,"Google Search query "+match+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True,pattern=r'.wiki (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern=r'.wiki (.*)'))
async def wiki(e):
        match = e.pattern_match.group(1)
        result=wikipedia.summary(match)
        await bot.send_message(await bot.get_input_entity(e.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=e.id, link_preview=False)
        await bot.send_message(-1001200493978,"Wiki query "+match+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.iamafk'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.iamafk'))
async def set_afk(e):
            message=e.text
            string = str(message[8:])
            global ISAFK
            global AFKREASON
            ISAFK=True
            await e.edit("AFK AF!")
            if string!="":
                AFKREASON=string
@bot.on(events.NewMessage(outgoing=True, pattern='.zal'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.iamafk'))
async def zal(e):
     textx=await e.get_reply_message()
     message = e.text
     if textx:
         message = textx
         message = str(message.message)
     else:
        message = str(message[4:])
     input_text = " ".join(message).lower()
     zalgofied_text = zalgo.zalgo().zalgofy(input_text)
     await e.edit(zalgofied_text)
@bot.on(events.NewMessage(outgoing=True, pattern='.asmon'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.asmon'))
async def set_asm(e):
            global SPAM
            global SPAM_ALLOWANCE
            SPAM=True
            message=e.text
            SPAM_ALLOWANCE=int(message[6:])
            await e.edit("Spam Tracking turned on!")
@bot.on(events.NewMessage(outgoing=True, pattern='.eval'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.eval'))
async def evaluate(e):
    evaluation = eval(e.text[6:])
    if inspect.isawaitable(evaluation):
       evaluation = await evaluation
    if evaluation:
      await e.edit("**Query: **\n`"+e.text[6:]+'`\n**Result: **\n`'+str(evaluation)+'`')
    else:
      await e.edit("**Query: **\n`"+e.text[6:]+'`\n**Result: **\n`No Result Returned/False`')
    await bot.send_message(-1001200493978,"Eval query "+e.text[6:]+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern=r'.exec (.*)'))
async def run(e):
 code = e.raw_text[5:]
 exec(
  f'async def __ex(e): ' +
  ''.join(f'\n {l}' for l in code.split('\n'))
 )
 result = await locals()['__ex'](e)
 if result:
  await e.edit("**Query: **\n`"+e.text[5:]+'`\n**Result: **\n`'+str(result)+'`')
 else:
  await e.edit("**Query: **\n`"+e.text[5:]+'`\n**Result: **\n`'+'No Result Returned/False'+'`')
 await bot.send_message(-1001200493978,"Exec query "+e.text[5:]+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.spam'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.spam'))
async def spammer(e):
    message= e.text
    counter=int(message[6:8])
    spam_message=str(e.text[8:])
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    await e.delete()
    await bot.send_message(-1001200493978,"Spam was executed successfully")
@bot.on(events.NewMessage(outgoing=True,pattern='.shutdown'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.shutdown'))
async def killdabot(e):
        message = e.text
        counter=int(message[10:])
        await e.reply('`Goodbye (*Windows XP showdown sound*....`')
        time.sleep(2)
        time.sleep(counter)
@bot.on(events.NewMessage(outgoing=True, pattern='.help'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.help'))
async def help(e):
    await e.edit('https://github.com/baalajimaestro/Telegram-UserBot/blob/master/README.md')
@bot.on(events.NewMessage(outgoing=True, pattern='.bigspam'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.bigspam'))
async def bigspam(e):
    message = e.text
    counter=int(message[9:13])
    spam_message=str(e.text[13:])
    for i in range (1,counter):
       await e.respond(spam_message)
    await e.delete()
    await bot.send_message(-1001200493978,"bigspam was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.trt'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.trt'))
async def translateme(e):
    translator=Translator()
    textx=await e.get_reply_message()
    message = e.text
    if textx:
         message = textx
         text = str(message.message)
    else:
        text = str(message[4:])
    reply_text=translator.translate(text, dest='en').text
    reply_text="`Source: `\n"+text+"`\n\nTranslation: `\n"+reply_text
    await bot.send_message(e.chat_id,reply_text)
    await e.delete()
    await bot.send_message(-1001200493978,"Translate query "+message+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.str'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.str'))
async def stretch(e):
    textx=await e.get_reply_message()
    message = e.text
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[5:])
    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message)
    await e.edit(reply_text)
@bot.on(events.NewMessage(incoming=True))
async def afk_on_pm(e):
    global ISAFK
    global USERS
    global COUNT_MSG
    global AFKREASON
    if e.is_private:
        if ISAFK:
            if (await e.get_sender()):
              if (await e.get_sender()).username not in USERS:
                  USERS.update({(await e.get_sender()).username:1})
                  COUNT_MSG=COUNT_MSG+1
                  await e.reply("AFK AF `"+AFKREASON+"`Spam me if you want me to notice you")
                  time.sleep(10)
                  i=1
                  async for message in bot.iter_messages(e.chat_id,from_user='me'):
                    if i>1:
                        break
                    i=i+1
                    await message.delete()
              elif (await e.get_sender()).username in USERS:
                     USERS[(await e.get_sender()).username]=USERS[(await e.get_sender()).username]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await e.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await e.reply("Bot is down. A better version of it, must be up now!")
            else:
                  USERS.update({e.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
                  await e.reply("AFK AF `"+AFKREASON+"`Spam me if you want me to notice you")
                  time.sleep(10)
                  i=1
                  async for message in bot.iter_messages(e.chat_id,from_user='me'):
                        if i>1:
                           break
                        i=i+1
                        await message.delete()
                  if e.chat_id in USERS:
                     USERS[e.chat_id]=USERS[e.chat_id]+1
                     COUNT_MSG=COUNT_MSG+1
                     textx=await e.get_reply_message()
                     if textx:
                         message = textx
                         text = str(message.message)
                         await e.reply("Dead")
@bot.on(events.NewMessage(outgoing=True, pattern='.cp'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.cp'))
async def copypasta(e):
    textx=await e.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = e.text
        message = str(message[3:])
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
    await e.edit(reply_text)
@bot.on(events.NewMessage(outgoing=True, pattern='.vapor'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.vapor'))
async def vapor(e):
    textx=await e.get_reply_message()
    message = e.text
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[7:])
    if message:
        data = message
    else:
        data = ''
    reply_text = str(data).translate(WIDE_MAP)
    await e.edit(reply_text)
@bot.on(events.NewMessage(outgoing=True, pattern='.sd'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.sd'))
async def selfdestruct(e):
    message=e.text
    counter=int(message[4:6])
    text=str(e.text[6:])
    text=text+"`This message shall be self-destructed in "+str(counter)+" seconds`"
    await e.delete()
    await bot.send_message(e.chat_id,text)
    time.sleep(counter)
    i=1
    async for message in bot.iter_messages(e.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
        await bot.send_message(-1001200493978,"sd query done successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='^.ud (.*)'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.ud (.*)'))
async def ud(e):
  await e.edit("Processing...")
  str = e.pattern_match.group(1)
  mean = urbandict.define(str)
  if len(mean) >= 0:
    await e.edit('Text: **'+str+'**\n\nMeaning: **'+mean[0]['def']+'**\n\n'+'Example: \n__'+mean[0]['example']+'__')
    await bot.send_message(-1001200493978,"ud query "+str+" executed successfully.")
  else:
    await e.edit("No result found for **"+str+"**")
@bot.on(events.NewMessage(outgoing=True, pattern='.tts'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.tts'))
async def tts(e):
    textx=await e.get_reply_message()
    replye = e.text
    if textx:
         replye = await e.get_reply_message()
         replye = str(replye.message)
    else:
        replye = str(replye[5:])
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    tts = gTTS(replye, "en-in")
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:                          #tts on personal chats is broken
        tts = gTTS(replyes,"en-in")
        tts.save("k.mp3")
    with open("k.mp3", "r") as speech:
        await bot.send_file(e.chat_id, 'k.mp3', voice_note=True)
        os.remove("k.mp3")
        await e.delete()
@bot.on(events.NewMessage(outgoing=True, pattern='.loltts'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.loltts'))
async def meme_tts(e):
    textx=await e.get_reply_message()
    replye = e.text
    if textx:
         replye = await e.get_reply_message()
         replye = str(replye.message)
    else:
        replye = str(replye[8:])
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    tts = gTTS(replye, "ja")
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:                          #tts on personal chats is broken
        tts = gTTS(replyes,"ja")
        tts.save("k.mp3")
    with open("k.mp3", "r") as speech:
        await bot.send_file(e.chat_id, 'k.mp3', voice_note=True)
        os.remove("k.mp3")
        await e.delete()
if len(sys.argv) < 2:
    bot.run_until_disconnected()

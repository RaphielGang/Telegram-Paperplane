import hastebin
import pybase64
import random,re,os,signal
import subprocess
from userbot import bot
from telethon import TelegramClient, events
from userbot import LOGGER,LOGGER_GROUP


@bot.on(events.NewMessage(outgoing=True,pattern='^.pip (.+)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.pip (.+)'))
async def pipcheck(e):
 if not e.text[0].isalpha():
    a=await e.reply('`Searching . . .`')
    r='`' + subprocess.run(['pip3', 'search', e.pattern_match.group(1)], stdout=subprocess.PIPE).stdout.decode() + '`'
    await e.edit(r)


@bot.on(events.NewMessage(outgoing=True,pattern='^.paste?(\\s)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.paste?(\\s)'))
async def haste_paste(e):
 if not e.text[0].isalpha():
    message=e.text
    await e.edit('`Pasting text . . .`')
    text=str(message[7:])
    await e.edit('`Paste successful! Check it here: `' + hastebin.post(text))


@bot.on(events.NewMessage(outgoing=True, pattern='^.log?(\\s)'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.log?(\\s)'))
async def log(e):
 if not e.text[0].isalpha():
    textx=await e.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = e.text
        message = str(message[4:])
    if LOGGER:
        await (await e.get_reply_message()).forward_to(LOGGER_GROUP)
        await e.edit("`Logged Successfully`")


@bot.on(events.NewMessage(outgoing=True, pattern='^.speed$'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.speed$'))
async def speedtest(e):
     if not e.text[0].isalpha():
            l=await e.reply('`Running speed test . . .`')
            k=subprocess.run(['speedtest-cli'], stdout=subprocess.PIPE)
            await l.edit('`' + k.stdout.decode()[:-1] + '`')
            await e.delete()


@bot.on(events.NewMessage(outgoing=True,pattern='^.hash (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.hash (.*)'))
async def hash(e):
 if not e.text[0].isalpha():
    hashtxt_ = e.pattern_match.group(1)
    hashtxt=open('hashdis.txt','w+')
    hashtxt.write(hashtxt_)
    hashtxt.close()
    md5=subprocess.run(['md5sum', 'hashdis.txt'], stdout=subprocess.PIPE)
    md5=md5.stdout.decode()
    sha1=subprocess.run(['sha1sum', 'hashdis.txt'], stdout=subprocess.PIPE)
    sha1=sha1.stdout.decode()
    sha256=subprocess.run(['sha256sum', 'hashdis.txt'], stdout=subprocess.PIPE)
    sha256=sha256.stdout.decode()
    sha512=subprocess.run(['sha512sum', 'hashdis.txt'], stdout=subprocess.PIPE)
    subprocess.run(['rm', 'hashdis.txt'], stdout=subprocess.PIPE)
    sha512=sha512.stdout.decode()
    ans='Text: `' + hashtxt_ + '`\nMD5: `' + md5 + '`SHA1: `' + sha1 + '`SHA256: `' + sha256 + '`SHA512: `' + sha512[:-1] + '`'
    if len(ans) > 4096:
        f=open('hashes.txt', 'w+')
        f.write(ans)
        f.close()
        await bot.send_file(e.chat_id, 'hashes.txt', reply_to=e.id, caption="`It's too big, in a text file and hastebin instead. `" + hastebin.post(ans[1:-1]))
        subprocess.run(['rm', 'hashes.txt'], stdout=subprocess.PIPE)
    else:
        await e.reply(ans)


@bot.on(events.NewMessage(outgoing=True,pattern='^.base64 (en|de) (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.base64 (en|de) (.*)'))
async def endecrypt(e):
 if not e.text[0].isalpha():
     if e.pattern_match.group(1) == 'en':
         lething=str(pybase64.b64encode(bytes(e.pattern_match.group(2), 'utf-8')))[2:]
         await e.reply('Encoded: `' + lething[:-1] + '`')
     else:
         lething=str(pybase64.b64decode(bytes(e.pattern_match.group(2), 'utf-8'), validate=True))[2:]
         await e.reply('Decoded: `' + lething[:-1] + '`')


@bot.on(events.NewMessage(outgoing=True, pattern='^.random'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.random'))
async def randomise(e):
  if not e.text[0].isalpha():
    r=(e.text).split()
    index=random.randint(1,len(r)-1)
    await e.edit("**Query: **\n`"+e.text+'`\n**Output: **\n`'+r[index]+'`')


@bot.on(events.NewMessage(outgoing=True,pattern='^.alive$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.alive$'))
async def amialive(e):
    if not e.text[0].isalpha():
        await e.edit("`Master! I am alive😁`")


@bot.on(events.NewMessage(outgoing=True,pattern='^.chatid$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.chatid$'))
async def chatidgetter(e):
    if not e.text[0].isalpha():
        await e.edit('Chat ID: `'+str(e.chat_id)+'`')


@bot.on(events.NewMessage(outgoing=True,pattern='^.restart$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.restart$'))
async def restart_the_bot(e):
	await e.edit("`Thank You master! I am taking a break!`")


	os.execl(sys.executable, sys.executable, *sys.argv)
@bot.on(events.NewMessage(outgoing=True,pattern='^.pingme$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.pingme$'))
async def pingme(e):
 if not e.text[0].isalpha():
    k=subprocess.run(['ping','-c','3','google.com'], stdout=subprocess.PIPE)
    await e.edit('`' + k.stdout.decode()[:-1] + '`')


@bot.on(events.NewMessage(outgoing=True,pattern='^.shutdown'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.shutdown'))
async def killdabot(e):
    if not e.text[0].isalpha():
        message = e.text
        counter=int(message[10:])
        await e.reply('`Goodbye *Windows XP shutdown sound*....`')
        time.sleep(2)
        await bot.send_message(LOGGER_GROUP,"You shutdown the bot for "+str(counter)+" seconds")
        time.sleep(counter)


@bot.on(events.NewMessage(outgoing=True,pattern='.support'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.support'))
async def bot_support(e):
    if not e.text[0].isalpha():
        await e.edit("Report bugs here: @userbot_support")


@bot.on(events.NewMessage(outgoing=True,pattern='^.repo$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.repo$'))
async def repo_is_here(e):
    if not e.text[0].isalpha():
        await e.edit('https://github.com/baalajimaestro/Telegram-UserBot/')


@bot.on(events.NewMessage(outgoing=True,pattern='^.supportchannel$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.supportchannel$'))
async def support_channel(e):
    if not e.text[0].isalpha():
        await e.edit('t.me/maestro_userbot_channel')


@bot.on(events.NewMessage(outgoing=True,pattern='^.sysdetails$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.sysdetails$'))
async def sysdetails(e):
    if not e.text[0].isalpha():
        r='`' + subprocess.run(['neofetch', '--off', '--color_blocks off', '--bold off', '--cpu_temp', 'C', '--cpu_speed','on','--cpu_cores', 'physical','--stdout'], stdout=subprocess.PIPE).stdout.decode() + '`'
        await e.edit(r)


@bot.on(events.NewMessage(outgoing=True,pattern='^.botversion$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.botversion$'))
async def bot_ver(e):
    if not e.text[0].isalpha():
        await e.edit('`UserBot Version: Modular r2.05`')

        
@bot.on(events.NewMessage(outgoing=True,pattern='^.userid$'))
@bot.on(events.MessageEdited(outgoing=True,pattern='^.userid$'))
async def chatidgetter(e):
    if not e.text[0].isalpha():
        await e.edit('User ID: `'+str((await e.get_reply_message()).sender_id)+'`')

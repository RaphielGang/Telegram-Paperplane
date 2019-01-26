import hastebin
import pybase64
import random, re, os, signal, io
import subprocess, time, sys
from userbot import bot
import time
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from userbot.modules.rextester.api import UnknownLanguage, Rextester
from userbot import LOGGER, LOGGER_GROUP


@bot.on(events.NewMessage(outgoing=True, pattern="^.pip (.+)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.pip (.+)"))
async def pipcheck(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        a = await e.reply("`Searching . . .`")
        r = (
            "`"
            + subprocess.run(
                ["pip3", "search", e.pattern_match.group(1)], stdout=subprocess.PIPE
            ).stdout.decode()
            + "`"
        )
        await e.edit(r)


######Will put del.dog later lmao sorry Tillie
@bot.on(events.NewMessage(outgoing=True, pattern="^.paste?(\\s)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.paste?(\\s)"))
async def haste_paste(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        await e.edit("`Pasting text . . .`")
        text = str(message[7:])
        await e.edit("`Paste successful! Check it here: `" + hastebin.post(text))


@bot.on(events.NewMessage(outgoing=True, pattern="^.log"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.log"))
async def log(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = textx
        message = str(message.message)
        if LOGGER:
            await (await e.get_reply_message()).forward_to(LOGGER_GROUP)
            await e.edit("`Logged Successfully`")
        else:
            await e.edit("`This feature requires Logging to be enabled!`")
        time.sleep(2)
        await e.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.speed$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.speed$"))
async def speedtest(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        l = await e.reply("`Running speed test . . .`")
        k = subprocess.run(["speedtest-cli"], stdout=subprocess.PIPE)
        await l.edit("`" + k.stdout.decode()[:-1] + "`")
        await e.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.hash (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.hash (.*)"))
async def hash(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        hashtxt_ = e.pattern_match.group(1)
        hashtxt = open("hashdis.txt", "w+")
        hashtxt.write(hashtxt_)
        hashtxt.close()
        md5 = subprocess.run(["md5sum", "hashdis.txt"], stdout=subprocess.PIPE)
        md5 = md5.stdout.decode()
        sha1 = subprocess.run(["sha1sum", "hashdis.txt"], stdout=subprocess.PIPE)
        sha1 = sha1.stdout.decode()
        sha256 = subprocess.run(["sha256sum", "hashdis.txt"], stdout=subprocess.PIPE)
        sha256 = sha256.stdout.decode()
        sha512 = subprocess.run(["sha512sum", "hashdis.txt"], stdout=subprocess.PIPE)
        subprocess.run(["rm", "hashdis.txt"], stdout=subprocess.PIPE)
        sha512 = sha512.stdout.decode()
        ans = (
            "Text: `"
            + hashtxt_
            + "`\nMD5: `"
            + md5
            + "`SHA1: `"
            + sha1
            + "`SHA256: `"
            + sha256
            + "`SHA512: `"
            + sha512[:-1]
            + "`"
        )
        if len(ans) > 4096:
            f = open("hashes.txt", "w+")
            f.write(ans)
            f.close()
            await bot.send_file(
                e.chat_id,
                "hashes.txt",
                reply_to=e.id,
                caption="`It's too big, in a text file and hastebin instead. `"
                + hastebin.post(ans[1:-1]),
            )
            subprocess.run(["rm", "hashes.txt"], stdout=subprocess.PIPE)
        else:
            await e.reply(ans)


@bot.on(events.NewMessage(outgoing=True, pattern="^.base64 (en|de) (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.base64 (en|de) (.*)"))
async def endecrypt(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.pattern_match.group(1) == "en":
            lething = str(pybase64.b64encode(bytes(e.pattern_match.group(2), "utf-8")))[
                2:
            ]
            await e.reply("Encoded: `" + lething[:-1] + "`")
        else:
            lething = str(
                pybase64.b64decode(
                    bytes(e.pattern_match.group(2), "utf-8"), validate=True
                )
            )[2:]
            await e.reply("Decoded: `" + lething[:-1] + "`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.random"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.random"))
async def randomise(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        r = (e.text).split()
        index = random.randint(1, len(r) - 1)
        await e.edit("**Query: **\n`" + e.text + "`\n**Output: **\n`" + r[index] + "`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.alive$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.alive$"))
async def amialive(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`Master! I am alive😁`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.chatid$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.chatid$"))
async def chatidgetter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Chat ID: `" + str(e.chat_id) + "`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.updatebleeding$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.updatebleding$"))
async def restart_the_bot(e):
    await e.edit("`Please wait while I upstream myself!`")
    bot.disconnect()
    try:
        subprocess.run(["python", "-m", "userbot", "test", "haha"])
    except:
        pass

@bot.on(events.NewMessage(outgoing=True, pattern="^.updatestable$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.updatestable$"))
async def restart_the_bot(e):
    await e.edit("`Please wait while I upstream myself!`")
    bot.disconnect()
    try:
        subprocess.run(["python", "-m", "userbot", "test", "haha", "yes"])
    except:
        pass

@bot.on(events.NewMessage(outgoing=True, pattern="^.pingme$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.pingme$"))
async def pingme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        start = datetime.now()
        await e.edit("`Pong!`")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await e.edit("Pong!\n%sms" % (ms))


@bot.on(events.NewMessage(outgoing=True, pattern="^.sleep( [0-9]+)?$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sleep( [0-9]+)?$"))
async def killdabot(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        if not " " in e.pattern_match.group(1):
            await e.reply("Syntax: `.shutdown [seconds]`")
        else:
            counter = int(e.pattern_match.group(1))
            await e.edit("`I am sulking and snoozing....`")
            time.sleep(2)
            await bot.send_message(
                LOGGER_GROUP,
                "You put the bot to sleep for " + str(counter) + " seconds",
            )
            time.sleep(counter)


@bot.on(events.NewMessage(outgoing=True, pattern="^.shutdown$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.shutdown$"))
async def killdabot(e):
    if not e.text[0].isalpha():
        await e.edit("`Goodbye *Windows XP shutdown sound*....`")
        await bot.send_message(LOGGER_GROUP, "You REALLY shutdown the bot")
        await bot.disconnect()


@bot.on(events.NewMessage(outgoing=True, pattern="^.support$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.support$"))
async def bot_support(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Report bugs here: @userbot_support")


@bot.on(events.NewMessage(outgoing=True, pattern="^.repo$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.repo$"))
async def repo_is_here(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/baalajimaestro/Telegram-UserBot/")


@bot.on(events.NewMessage(outgoing=True, pattern="^.supportchannel$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.supportchannel$"))
async def support_channel(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("t.me/maestro_userbot_channel")


@bot.on(events.NewMessage(outgoing=True, pattern="^.sysd$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sysd$"))
async def sysdetails(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        r = (
            "`"
            + subprocess.run(
                [
                    "neofetch",
                    "--off",
                    "--color_blocks off",
                    "--bold off",
                    "--cpu_temp",
                    "C",
                    "--cpu_speed",
                    "on",
                    "--cpu_cores",
                    "physical",
                    "--stdout",
                ],
                stdout=subprocess.PIPE,
            ).stdout.decode()
            + "`"
        )
        await e.edit(r)


@bot.on(events.NewMessage(outgoing=True, pattern="^.botver$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.botver$"))
async def bot_ver(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`UserBot Version: Modular r2.1.1-b`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.userid$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.userid$"))
async def chatidgetter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = await e.get_reply_message()
        if message:
            if not message.forward:
                user_id = message.sender.id
                if message.sender.username:
                    name = "@" + message.sender.username
                else:
                    name = "**" + message.sender.first_name + "**"

            else:
                user_id = message.forward.sender.id
                if message.forward.sender.username:
                    name = "@" + message.forward.sender.username
                else:
                    name = "*" + message.forward.sender.first_name + "*"
            await e.edit("**Name:** {} \n**User ID:** `{}`".format(name, user_id))

@bot.on(events.NewMessage(outgoing=True, pattern="^\$"))
async def rextestercli(e):
    stdin = ""
    message = e.text
    chat = await e.get_chat()

    if len(message.split()) > 1:
        regex = re.search(
            r"^\$([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$",
            message,
            re.IGNORECASE,
        )
        language = regex.group(1)
        code = regex.group(2)
        stdin = regex.group(3)

        try:
            rextester = Rextester(language, code, stdin)
            res = await rextester.exec()
        except UnknownLanguage as exc:
            await e.edit(str(exc))
            return

        output = ""
        output += f"**Language:**\n```{language}```"
        output += f"\n\n**Source:** \n```{code}```"

        if res.result:
            output += f"\n\n**Result:** \n```{res.result}```"

        if res.warnings:
            output += f"\n\n**Warnings:** \n```{res.warnings}```\n"

        if res.errors:
            output += f"\n\n**Errors:** \n'```{res.errors}```"

        if len(res.result) > 4096:
            with io.BytesIO(str.encode(res.result)) as out_file:
                out_file.name = "result.txt"
                await bot.send_file(chat.id, file = out_file)
                await e.edit(code)
            return

        await e.edit(output)


@bot.on(events.NewMessage(outgoing=True, pattern="^.unmutechat$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.unmutechat$"))
async def unmute_chat(e):
        if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
            try:
                from userbot.modules.sql_helper.keep_read_sql import unkread
            except:
                await e.edit('`Running on Non-SQL Mode!`')
            unkread(str(e.chat_id))
            await e.edit("```Unmuted this chat Successfully```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.mutechat$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.mutechat$"))
async def mute_chat(e):
        if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
            try:
                from userbot.modules.sql_helper.keep_read_sql import kread
            except Exception as er:
                print(er)
                await e.edit("`Running on Non-SQL mode!`")
                return
            await e.edit(str(e.chat_id))
            kread(str(e.chat_id))
            await e.edit("`Shush! This chat will be silenced!`")
            if LOGGER:
                await bot.send_message(
                    LOGGER_GROUP,
                    str(e.chat_id) + " was silenced.")


@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def keep_read(e):
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except:
        return
    K = is_kread()
    if K:
      for i in K:
        if i.groupid == str(e.chat_id):
            await bot.send_read_acknowledge(e.chat_id)


@bot.on(events.NewMessage(outgoing=True, pattern="^.botlog$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.botlog$"))
async def botlogs(e):
    process = await asyncio.create_subprocess_shell("sudo systemctl status userbot | tail -n 20", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip())
    f = open("err.log", "w+")
    f.write(result)
    f.close()
    await bot.send_file(
    e.chat_id,
    "sender.txt",
    reply_to=e.id,
    caption="`Bot logs are here!`",
    )

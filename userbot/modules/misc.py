# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

import random
import time
from asyncio import create_subprocess_shell as asyncsh
from asyncio.subprocess import PIPE as asyncsh_PIPE
from subprocess import PIPE
from subprocess import run as runapp

import hastebin
import pybase64
from requests import get, post

from userbot.events import register
from userbot import LOGGER, LOGGER_GROUP

DOGBIN_URL = "https://del.dog/"


@register(outgoing=True, pattern="^.paste")
async def paste(pstl):
    if not pstl.text[0].isalpha() and pstl.text[0] not in ("/", "#", "@", "!"):
        dogbin_final_url = ""

        textx = await pstl.get_reply_message()
        message = pstl.text
        await pstl.edit("`Pasting text . . .`")
        if message[7:]:
            message = str(message[7:])
        elif textx:
            message = str(textx.message)

        # Dogbin
        r = post(DOGBIN_URL + "documents", data=message.encode('utf-8'))

        if r.status_code == 200:
            response = r.json()
            key = response['key']
            dogbin_final_url = DOGBIN_URL + key

            if response['isUrl']:
                reply_text = (
                    "`Pasted successfully!`\n\n"
                    f"`Shortened URL:` {dogbin_final_url}\n\n`"
                    "Original(non-shortened) URLs`\n"
                    f"`Dogbin URL`: {DOGBIN_URL}v/{key}\n`")
            else:
                reply_text = (
                    "`Pasted successfully!`\n\n"
                    f"`Dogbin URL`: {dogbin_final_url}\n`")
        else:
            reply_text = (
                "`Failed to reach Dogbin`")

        await pstl.edit(reply_text)
        if LOGGER:
            await pstl.client.send_message(
                LOGGER_GROUP,
                "Paste query `" + message + "` was executed successfully",
            )


@register(outgoing=True, pattern="^.get_dogbin_content")
async def get_dogbin_content(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = e.text
        await e.edit("`Getting dogbin content . . .`")
        if message[7:]:
            message = str(message[20:])
        elif textx:
            message = str(textx.message)

        format_normal = f'{DOGBIN_URL}'
        format_view = f'{DOGBIN_URL}v/'

        if message.startswith(format_view):
            message = message[len(format_view):]
        elif message.startswith(format_normal):
            message = message[len(format_normal):]

        r = get(f'{DOGBIN_URL}raw/{message}')

        if r.status_code != 200:
            try:
                res = r.json()
                await e.reply(res['message'])
            except Exception:
                if r.status_code == 404:
                    await e.edit('`Failed to reach dogbin`')
                else:
                    await e.edit('`Unknown error occured`')
            r.raise_for_status()

        reply_text = "`Fetched dogbin URL content successfully!`\n\n`Content:` " + r.text

        await e.reply(reply_text)
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "Get dogbin content query for `" + message + "` was executed successfully",
            )


@register(outgoing=True, pattern="^.log")
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


@register(outgoing=True, pattern="^.hash (.*)")
async def hash(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        hashtxt_ = e.pattern_match.group(1)
        hashtxt = open("hashdis.txt", "w+")
        hashtxt.write(hashtxt_)
        hashtxt.close()
        md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
        md5 = md5.stdout.decode()
        sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
        sha1 = sha1.stdout.decode()
        sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
        sha256 = sha256.stdout.decode()
        sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
        runapp(["rm", "hashdis.txt"], stdout=PIPE)
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
            await e.client.send_file(
                e.chat_id,
                "hashes.txt",
                reply_to=e.id,
                caption="`It's too big, in a text file and hastebin instead. `"
                + hastebin.post(ans[1:-1]),
            )
            runapp(["rm", "hashes.txt"], stdout=PIPE)
        else:
            await e.reply(ans)


@register(outgoing=True, pattern="^.base64 (en|de) (.*)")
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


@register(outgoing=True, pattern="^.random")
async def randomise(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        r = (e.text).split()
        index = random.randint(1, len(r) - 1)
        await e.edit("**Query: **\n`" + e.text + "`\n**Output: **\n`" + r[index] + "`")


@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`Master! I am alive 😁`")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Chat ID: `" + str(e.chat_id) + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(e):
    message = e.text
    if not message[0].isalpha() and message[0] not in ("/", "#", "@", "!"):
        if " " not in e.pattern_match.group(1):
            await e.reply("Syntax: `.shutdown [seconds]`")
        else:
            counter = int(e.pattern_match.group(1))
            await e.edit("`I am sulking and snoozing....`")
            time.sleep(2)
            await e.client.send_message(
                LOGGER_GROUP,
                "You put the bot to sleep for " + str(counter) + " seconds",
            )
            time.sleep(counter)


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(e):
    if not e.text[0].isalpha():
        await e.edit("`Goodbye *Windows XP shutdown sound*....`")
        await e.client.send_message(LOGGER_GROUP, "You REALLY shutdown the bot")
        await e.client.disconnect()


@register(outgoing=True, pattern="^.support$")
async def bot_support(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Report bugs here: @userbot_support")


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/baalajimaestro/Telegram-UserBot/")


@register(outgoing=True, pattern="^.supportchannel$")
async def support_channel(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("t.me/maestro_userbot_channel")


@register(outgoing=True, pattern="^.userid$")
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
            await e.edit(
                "**Name:** {} \n**User ID:** `{}`"
                .format(name, user_id)
            )


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.keep_read_sql import unkread
        except:
            await e.edit('`Running on Non-SQL Mode!`')
        unkread(str(e.chat_id))
        await e.edit("```Unmuted this chat Successfully```")


@register(outgoing=True, pattern="^.mutechat$")
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
            await e.client.send_message(
                LOGGER_GROUP,
                str(e.chat_id) + " was silenced.")


@register(incoming=True)
async def keep_read(e):
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except:
        return
    K = is_kread()
    if K:
        for i in K:
            if i.groupid == str(e.chat_id):
                await e.client.send_read_acknowledge(e.chat_id)


@register(outgoing=True, pattern="^.botlog$")
async def botlogs(e):
    process = await asyncsh(
        "sudo systemctl status userbot | tail -n 20",
        stdout=asyncsh_PIPE,
        stderr=asyncsh_PIPE
        )

    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip())
    f = open("err.log", "w+")
    f.write(result)
    f.close()
    await e.client.send_file(
        e.chat_id,
        "err.log",
        reply_to=e.id,
        caption="`Bot logs are here!`",
    )

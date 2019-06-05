# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for interacting with dogbin(https://del.dog)"""

import json
from requests import get, post, exceptions

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOGS
from userbot.events import register

DOGBIN_URL = "https://del.dog/"


@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ For .paste command, allows using dogbin functionality with the command. """
    if not pstl.text[0].isalpha() and pstl.text[0] not in ("/", "#", "@", "!"):
        dogbin_final_url = ""
        match = pstl.pattern_match.group(1).strip()
        reply_id = pstl.reply_to_msg_id

        if not match and not reply_id:
            await pstl.edit("There's nothing to paste.")
            return

        if match:
            message = match
        elif reply_id:
            message = (await pstl.get_reply_message()).message

        # Dogbin
        await pstl.edit("`Pasting text . . .`")
        resp = post(DOGBIN_URL + "documents", data=message.encode('utf-8'))

        if resp.status_code == 200:
            response = resp.json()
            key = response['key']
            dogbin_final_url = DOGBIN_URL + key

            if response['isUrl']:
                reply_text = (
                    "`Pasted successfully!`\n\n"
                    f"`Shortened URL:` {dogbin_final_url}\n\n"
                    "Original(non-shortened) URLs`\n"
                    f"`Dogbin URL`: {DOGBIN_URL}v/{key}\n")
            else:
                reply_text = (
                    "`Pasted successfully!`\n\n"
                    f"`Dogbin URL`: {dogbin_final_url}")
        else:
            reply_text = (
                "`Failed to reach Dogbin`")

        await pstl.edit(reply_text)
        if BOTLOG:
            await pstl.client.send_message(
                BOTLOG_CHATID,
                "Paste query `" + message + "` was executed successfully",
            )


@register(outgoing=True, pattern="^.get_dogbin_content (.*)")
async def get_dogbin_content(dog_url):
    """ For .get_dogbin_content command, fetches the content of a dogbin URL. """
    if not dog_url.text[0].isalpha() and dog_url.text[0] not in ("/", "#", "@", "!"):
        textx = await dog_url.get_reply_message()
        message = dog_url.pattern_match.group(1)
        await dog_url.edit("`Getting dogbin content . . .`")
        
        if textx:
            message = str(textx.message)

        format_normal = f'{DOGBIN_URL}'
        format_view = f'{DOGBIN_URL}v/'

        if message.startswith(format_view):
            message = message[len(format_view):]
        elif message.startswith(format_normal):
            message = message[len(format_normal):]
        else:
            if message.startswith("del.dog/"):
                message = message[len("del.dog/"):]
            else:
                await dog_url.edit("`Are you sure you're using a valid dogbin URL?`")
                return

        resp = get(f'{DOGBIN_URL}raw/{message}')

        try:
            resp.raise_for_status()
        except exceptions.HTTPError as HTTPErr:
            await dog_url.edit("Request returned an unsuccessful status code.\n\n" + str(HTTPErr))
            return
        except exceptions.Timeout as TimeoutErr:
            await dog_url.edit("Request timed out."+ str(TimeoutErr))
            return
        except exceptions.TooManyRedirects as RedirectsErr:
            await dog_url.edit("Request exceeded the configured number of maximum redirections." + str(RedirectsErr))
            return

        reply_text = "`Fetched dogbin URL content successfully!`\n\n`Content:` " + resp.text

        await dog_url.reply(reply_text)
        if BOTLOG:
            await dog_url.client.send_message(
                BOTLOG_CHATID,
                "Get dogbin content query for `" + message + "` was executed successfully",
            )

CMD_HELP.update({
    "paste": "Create a paste or a shortened url using dogbin (https://del.dog/)"
})
CMD_HELP.update({
    "get_dogbin_content": "Get the content of a paste or shortened url from dogbin (https://del.dog/)"
})
CMD_HELP.update({
    "pastestats": "Get stats of a paste or shortened url from dogbin (https://del.dog/)"
})

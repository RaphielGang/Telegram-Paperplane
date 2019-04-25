# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#\
""" Userbot module containing commands for interacting with dogbin(https://del.dog)"""

import json
from requests import get, post

from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register

DOGBIN_URL = "https://del.dog/"


@register(outgoing=True, pattern="^.paste")
async def paste(pstl):
    """ For .paste command, allows using dogbin functionality with the command. """
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
        if LOGGER:
            await pstl.client.send_message(
                LOGGER_GROUP,
                "Paste query `" + message + "` was executed successfully",
            )


@register(outgoing=True, pattern="^.get_dogbin_content")
async def get_dogbin_content(dog_url):
    """ For .get_dogbin_content command, fetches the content of a dogbin URL. """
    if not dog_url.text[0].isalpha() and dog_url.text[0] not in ("/", "#", "@", "!"):
        textx = await dog_url.get_reply_message()
        message = dog_url.text
        await dog_url.edit("`Getting dogbin content . . .`")
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

        resp = get(f'{DOGBIN_URL}raw/{message}')

        if resp.status_code != 200:
            try:
                res = resp.json()
                await dog_url.reply(res['message'])
            except json.decoder.JSONDecodeError:
                if resp.status_code == 404:
                    await dog_url.edit('`Failed to reach dogbin`')
                else:
                    await dog_url.edit('`Unknown error occured`')
            resp.raise_for_status()

        reply_text = "`Fetched dogbin URL content successfully!`\n\n`Content:` " + resp.text

        await dog_url.reply(reply_text)
        if LOGGER:
            await dog_url.client.send_message(
                LOGGER_GROUP,
                "Get dogbin content query for `" + message + "` was executed successfully",
            )

HELPER.update({
    "paste": "Create a paste or a shortened url using dogbin (https://del.dog/)"
})
HELPER.update({
    "get_dogbin_content": "Get the content of a paste or shortened url from dogbin (https://del.dog/)"
})
HELPER.update({
    "pastestats": "Get stats of a paste or shortened url from dogbin (https://del.dog/)"
})

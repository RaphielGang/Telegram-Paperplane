# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands
    for interacting with Katbin (https://katb.in)"""

import json
from requests import exceptions, get, post

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register, grp_exclude

KATBIN_URL = "katb.in/"
KATBIN_API_URL = "https://api.katb.in/api/paste/"


@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
@grp_exclude()
async def paste(pstl):
    """For .paste command, allows using
    Katbin functionality with the command."""

    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id
    if not match and not reply_id:
        await pstl.edit("There's nothing to paste.")
        return

    if match:
        message = match
    elif reply_id:
        message = (await pstl.get_reply_message()).message

    # Katbin
    await pstl.edit("`Pasting text...`")
    resp = post(
        KATBIN_API_URL,
        headers={"content-type": "application/json"},
        data=json.dumps({"content": message}),
    )

    if resp.status_code == 201:
        response = resp.json()
        key = response["paste_id"]

        reply_text = "`Pasted!`\n\n" f"`Katbin URL:` https://{KATBIN_URL}{key}"
    else:
        reply_text = "`Failed to reach Katbin`"

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID, "Paste query `" + message + "` was executed successfully"
        )


@register(outgoing=True, pattern=r"^.getpaste(?: |$)(.*)")
@grp_exclude()
async def getpaste(paste_url):
    """For .getpaste command,
    fetches the content of a Katbin URL."""
    textx = await paste_url.get_reply_message()
    message = paste_url.pattern_match.group(1)
    await paste_url.edit("`Getting Katbin content . . .`")

    if textx:
        message = str(textx.message)

    for startstr in [
        f"https://{KATBIN_URL}v/",
        f"{KATBIN_URL}v/",
        f"https://{KATBIN_URL}",
        KATBIN_URL,
    ]:
        if message.startswith(startstr):
            pasteid = message[len(startstr) :]
            break
    else:
        await paste_url.edit("`Are you sure you're using a valid Katbin URL?`")
        return

    resp = get(f"{KATBIN_API_URL}{pasteid}")

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await paste_url.edit(
            "Request returned an unsuccessful status code.\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await paste_url.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await paste_url.edit(
            "Request exceeded the configured \
                        number of maximum redirections."
            + str(RedirectsErr)
        )
        return

    response = resp.json()
    reply_text = "`Fetched Katbin URL content "
    reply_text += "successfully!`\n\n`Content:` " + response["content"]

    await paste_url.edit(reply_text)
    if BOTLOG:
        await paste_url.client.send_message(
            BOTLOG_CHATID,
            "Get Katbin content query for `" + message + "` was executed successfully",
        )


CMD_HELP.update(
    {
        "paste": [
            "Paste",
            " - `.paste`: Create a paste or a shortened URL using Katbin (https://katb.in/).\n"
            " - `.getpaste`: Get the content of a paste or shortened URL from Katbin (https://katb.in/).\n",
        ]
    }
)

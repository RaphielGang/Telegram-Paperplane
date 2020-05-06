# Copyright (C) 2019 The Raphielscape Company LLC, Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for ScreenshotLayer API """

import os

from requests import get

from userbot import CMD_HELP, SCREENSHOT_LAYER_ACCESS_KEY
from userbot.events import register


BASEURL = "https://api.screenshotlayer.com/api/capture"


@register(pattern=r"^.screencapture (.*)", outgoing=True)
async def capture(url):
    """ For .screencapture command, capture a website and send the photo. """
    if SCREENSHOT_LAYER_ACCESS_KEY is None:
        await url.edit("Invalid Api Key")
        return
    imglink = url.pattern_match.group(1)
    parameterz = {"access_key": SCREENSHOT_LAYER_ACCESS_KEY, "url": imglink, "fullpage": "1",
                  "format": "PNG", "viewport": "2560x1440"}
    resp = get(BASEURL, stream=True, params=parameterz)
    content_type = resp.headers["content-type"]
    if "image" in content_type:
        temp = "screencapture.png"
        with open(temp, "wb") as file:
            for chunk in resp.iter_content(chunk_size=128):
                file.write(chunk)
        try:
            await url.client.send_file(
                url.chat_id,
                temp,
                caption=imglink,
                force_document=True,
                reply_to=url.message.reply_to_msg_id,
            )
            await url.delete()
        except BaseException:
            await url.edit(resp.text)
        os.remove(temp)
    else:
        await url.edit(resp.text)


CMD_HELP.update({"Screencapture":
    " - `.screencapture <url>`: Take a screenshot of a website and send it.\n"
})

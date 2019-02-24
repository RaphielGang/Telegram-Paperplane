# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

import os
import requests

from userbot import SCREENSHOT_LAYER_ACCESS_KEY
from userbot.events import register


@register(pattern=r".screencapture (.*)", outgoing=True)
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if SCREENSHOT_LAYER_ACCESS_KEY is None:
            await e.edit(
                "Need to get an API key from https://screenshotlayer.com/product \nModule stopping!"
            )
            return
        await e.edit("Processing ...")
        sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&format={}&viewport={}"
        input_str = e.pattern_match.group(1)
        response_api = requests.get(
            sample_url.format(
                SCREENSHOT_LAYER_ACCESS_KEY, input_str, "1", "PNG", "2560x1440"
            ),
            stream=True,
        )
        contentType = response_api.headers["content-type"]
        if "image" in contentType:
            temp_file_name = "screencapture.png"
            with open(temp_file_name, "wb") as fd:
                for chunk in response_api.iter_content(chunk_size=128):
                    fd.write(chunk)
            try:
                await e.client.send_file(
                    e.chat_id,
                    temp_file_name,
                    caption=input_str,
                    force_document=True,
                    reply_to=e.message.reply_to_msg_id,
                )
                await e.delete()
            except:
                await e.edit(response_api.text)
            os.remove(temp_file_name)
        else:
            await e.edit(response_api.text)

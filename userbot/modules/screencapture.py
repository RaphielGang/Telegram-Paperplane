# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import requests
from telethon import TelegramClient, events
from userbot import bot


@bot.on(events.NewMessage(pattern=r".screencapture (.*)", outgoing=True))
async def _(event):
  if not e.text[0].isalpha() and e.text[0]!="!" and e.text[0]!="/" and e.text[0]!="#" and e.text[0]!="@":
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}"
    input_str = event.pattern_match.group(1)
    response_api = requests.get(sample_url.format(SCREEN_SHOT_LAYER_ACCESS_KEY, input_str), stream=True)
    temp_file_name = "screenshotlayer.jpg"
    with open(temp_file_name, "wb") as fd:
        for chunk in response_api.iter_content(chunk_size=128):
            fd.write(chunk)
    try:
        await bot.send_file(
            event.chat_id,
            temp_file_name,
            caption=input_str,
            force_document=True,
            reply_to=event.message.reply_to_msg_id
        )
        await event.delete()
    except:
        await event.edit(response_api.text)
    os.remove(temp_file_name)

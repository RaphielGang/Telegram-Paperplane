# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import requests
import json

@bot.on(events.NewMessage(pattern=r".weather (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}"
    input_str = event.pattern_match.group(1)
    response_api = requests.get(sample_url.format(input_str, OPEN_WEATHER_MAP_APPID)).json()
    if response_api["cod"] == 200:
        await event.edit(input_str + "\n `" + json.dumps(response_api["main"]) + "`\n")
    else:
        await event.edit(response_api["message"])

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from datetime import datetime

import speedtest
from telethon import functions
from userbot import HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    if not spd.text[0].isalpha() and spd.text[0] not in ("/", "#", "@", "!"):
        await spd.edit("`Running speed test . . .`")
        test = speedtest.Speedtest()

        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()

    await spd.edit("`"
                   "Started at "
                   f"{result['timestamp']} \n\n"
                   "Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {
        0: '',
        1: 'Kb/s',
        2: 'Mb/s',
        3: 'Gb/s',
        4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.nearestdc$")
async def neardc(e):
    result = await e.client(functions.help.GetNearestDcRequest())
    await e.edit(
        f"Country : `{result.country}` \n"
        f"Nearest Datacenter : `{result.nearest_dc}` \n"
        f"This Datacenter : `{result.this_dc}`"
    )


@register(outgoing=True, pattern="^.pingme$")
async def pingme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        start = datetime.now()
        await e.edit("`Pong!`")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await e.edit("Pong!\n%sms" % (ms))

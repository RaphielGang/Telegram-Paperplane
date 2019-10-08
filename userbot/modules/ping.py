# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module to check latency of your bot. """


import datetime

from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.ping$")
async def ping(event):
    now = datetime.datetime.now()
    await event.edit('Pinging...')
    later = datetime.datetime.now()
    delta = later - now
    await event.edit('Pong!\n' + str(int(delta.total_seconds() * 1000)) + 'ms' )

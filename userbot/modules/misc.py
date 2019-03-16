# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD

from random import randint
from subprocess import PIPE
from subprocess import run as runapp
from time import sleep

import hastebin
import pybase64
from requests import get, post

from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.random")
async def randomise(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        r = (e.text).split()
        index = randint(1, len(r) - 1)
        await e.edit("**Query: **\n`" + e.text + "`\n**Output: **\n`" + r[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(e):
    message = e.text
    if not message[0].isalpha() and message[0] not in ("/", "#", "@", "!"):
        if " " not in e.pattern_match.group(1):
            await e.reply("Syntax: `.sleep [seconds]`")
        else:
            counter = int(e.pattern_match.group(1))
            await e.edit("`I am sulking and snoozing....`")
            sleep(2)
            if LOGGER:
                await e.client.send_message(
                    LOGGER_GROUP,
                    "You put the bot to sleep for " + str(counter) + " seconds",
                )
            sleep(counter)


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(e):
    if not e.text[0].isalpha():
        await e.edit("`Goodbye *Windows XP shutdown sound*....`")
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "#SHUTDOWN \n"
                "Bot shutted down")
        await e.client.disconnect()


@register(outgoing=True, pattern="^.support$")
async def bot_support(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Link Portal: @userbot_support")


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/baalajimaestro/Telegram-UserBot/")
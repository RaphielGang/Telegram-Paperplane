# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import sys
from os import execl, environ, execle
from random import randint
from time import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()

    if len(itemo) < 2:
        await items.edit("`2 or more items are required! Check "
                         ".help random for more info.`")
        return

    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    if " " not in time.pattern_match.group(1):
        await time.reply("Syntax: `.sleep [seconds]`")
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit("`I am sulking and snoozing....`")
        sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "You put the bot to sleep for " + str(counter) + " seconds",
            )
        sleep(counter)


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Goodbye *Windows XP shutdown sound*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                                       "Bot shut down")
    await event.client.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def knocksomesense(event):
    await event.edit("`Hold tight! I just need a second to be back up....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                                       "Bot Restarted")
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit("https://github.com/HitaloSama/PaperplaneMinimal/")


CMD_HELP.update({"misc": ["Misc",
                          " - `random` <item1> <item2> ... <itemN>: Get a random item from the list of items.\n"
                          " - `sleep` <secs>: Paperpane gets tired too. Let yours snooze for a few seconds.\n"
                          " - `shutdown`: Sometimes you need to turn Paperplane off. Sometimes you just hope to"
                          "hear Windows XP shutdown sound... but you don't.\n"
                          " - `restart`: Restarts the userbot\n"
                          " - `repo`: Get the link of the source code of Paperplane in GitHub.\n\n"
                          "**All commands can be used with** `.`"]
                 })

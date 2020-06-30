# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import sys
from os import execl
from random import randint
from time import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register, grp_exclude


@register(outgoing=True, pattern="^.random")
@grp_exclude()
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
@grp_exclude()
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
@grp_exclude()
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Goodbye *Windows XP shutdown sound*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot shut down")
    await event.client.disconnect()


@register(outgoing=True, pattern="^.restart$")
@grp_exclude()
async def knocksomesense(event):
    await event.edit("`Hold tight! I just need a second to be back up....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot Restarted")
    await event.client.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


@register(outgoing=True, pattern="^.support$")
@grp_exclude()
async def bot_support(wannahelp):
    """ For .support command, just returns the group link. """
    await wannahelp.edit("Group: @tgpaperplane")


@register(outgoing=True, pattern="^.repo$")
@grp_exclude()
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit("https://github.com/RaphielGang/Telegram-UserBot/")


CMD_HELP.update({
    "misc": [
        "Misc",
        " - `.random <item1> <item2> ... <itemN>`: Get a random item from the list of items.\n"
        " - `.sleep <secs>`: Paperpane gets tired too. Let yours snooze for a few seconds.\n"
        " - `.shutdown`: Sometimes you need to turn Paperplane off. Sometimes you just hope to"
        "hear Windows XP shutdown sound... but you don't.\n"
        " - `.support`: If you need more help, use this command.\n"
        " - `.repo`: Get the link of the source code of Paperplane in GitHub.\n"
    ]
})

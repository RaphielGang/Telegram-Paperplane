# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
@errors_handler
async def help(event):
    """ For .help command,"""
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        args = event.pattern_match.group(1)
        if args:
            if args in CMD_HELP:
                await event.edit(str(CMD_HELP[args]))
            else:
                await event.edit("Please specify a valid module name.")
        else:
            await event.edit(
                "Please specify which module do you want help for!")
            string = ""
            for i in CMD_HELP:
                string += "`" + str(i)
                string += "`\n"
            await event.reply(string)

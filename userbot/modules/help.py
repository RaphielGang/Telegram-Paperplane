# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    """ For .help command,"""
    args = event.pattern_match.group(1).title()

    if args:
        if args in CMD_HELP:
            try:
                await event.edit(f"Here is the help for the **{args}** module:\n\n" + str(CMD_HELP[args]))
            except:
                pass
        else:
            try:
                await event.edit("Please specify a valid module name.")
            except:
                pass
    else:
        try:
            await event.edit(
                "Please specify which module you want help for!")
            string = ""
            for i in CMD_HELP:
                string += "`" + str(i)
                string += "`, "
            string = string[:-2]
            await event.reply(string)
        except:
            pass

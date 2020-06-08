# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Paperplane's help command """

from userbot import CMD_HELP
from userbot.events import register, grp_exclude


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
@grp_exclude()
async def help(event):
    """ For .help command"""
    args = event.pattern_match.group(1).lower()

    if args:
        if args in CMD_HELP:
            await event.edit(
                f"Here is some help for the **{CMD_HELP[args][0]}** module:\n\n"
                + str(CMD_HELP[args][1]))
        else:
            await event.edit(
                f"Help string for {args} not found! Type ```.help``` to see valid module names."
            )
    else:
        string = ""
        for i in CMD_HELP.values():
            string += f"`{str(i[0])}`, "
        string = string[:-2]
        await event.edit("Please specify which module you want help for!\n\n"
                         f"{string}")

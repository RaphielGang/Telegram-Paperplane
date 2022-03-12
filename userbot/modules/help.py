# Copyright (C) 2019-2022 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Paperplane's help command """

from userbot import CMD_HELP
from userbot.events import register, grp_exclude


@register(outgoing=True, pattern=r"^.help(?: |$)(.*)")
@grp_exclude()
async def help_cmd(event):
    """For .help command"""
    args = event.pattern_match.group(1).lower()

    if not args:
        string = "\n".join([f"`{x[0]}`" for x in CMD_HELP.values()])
        return await event.edit(
            f"Please specify which module you want help for!\n\n{string}"
        )

    if args in CMD_HELP:
        await event.edit(
            f"Here is some help for the **{CMD_HELP[args][0]}** module:\n\n{CMD_HELP[args][1]}"
        )
    else:
        await event.edit(
            f"Help string for {args} not found! Type `.help` to see valid module names."
        )

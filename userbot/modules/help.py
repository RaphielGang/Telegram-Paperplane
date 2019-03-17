# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register

@register(outgoing=True, pattern="^.help")
async def help(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        s = e.text.split()
        if len(s) == 2:
            if HELPER[s[1]]:
                await e.edit(str(HELPER[s[1]]))
        else:
            t = await e.edit("Please specify which module do you want help for!")
            string = ""
            print(HELPER.keys())
            for i in HELPER.keys():
                string += str(i)
                string += "\n"
            await t.reply(string)
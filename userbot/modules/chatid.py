# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.


from time import sleep

from userbot import HELPER, LOGGER, LOGGER_GROUP
from userbot.events import register


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = await e.get_reply_message()
        if message:
            if not message.forward:
                user_id = message.sender.id
                if message.sender.username:
                    name = "@" + message.sender.username
                else:
                    name = "**" + message.sender.first_name + "**"

            else:
                user_id = message.forward.sender.id
                if message.forward.sender.username:
                    name = "@" + message.forward.sender.username
                else:
                    name = "*" + message.forward.sender.first_name + "*"
            await e.edit(
                "**Name:** {} \n**User ID:** `{}`"
                .format(name, user_id)
            )


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Chat ID: `" + str(e.chat_id) + "`")


@register(outgoing=True, pattern="^.log")
async def log(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = textx
        message = str(message.message)
        if LOGGER:
            await (await e.get_reply_message()).forward_to(LOGGER_GROUP)
            await e.edit("`Logged Successfully`")
        else:
            await e.edit("`This feature requires Logging to be enabled!`")
        sleep(2)
        await e.delete()

HELPER.update({
    "chatid" : "Fetches the current chat's ID"
})

HELPER.update({
    "userid" : "Fetches the ID of the user in reply, if its a forwarded message, finds the ID for the source."
})

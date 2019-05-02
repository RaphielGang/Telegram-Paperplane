# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for muting chats. """

from userbot import LOGGER, LOGGER_GROUP, HELPER, MONGO
from userbot.events import register

@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ For .unmutechat command, unmute a muted chat. """
    if not unm_e.text[0].isalpha() and unm_e.text[0] not in ("/", "#", "@", "!"):
        try:
             from userbot import MONGO
        except AttributeError:
            await unm_e.edit('`Running on Non-SQL Mode!`')
            return
        MONGO.mute_chats.delete_one({
            "chat_id":unm_e.chat_id
            })
        await unm_e.edit("```Unmuted this chat Successfully```")


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ For .mutechat command, mute any chat. """
    if not mute_e.text[0].isalpha() and mute_e.text[0] not in ("/", "#", "@", "!"):
        try:
             from userbot import MONGO
        except AttributeError:
            await mute_e.edit("`Running on Non-SQL mode!`")
            return
        await mute_e.edit(str(mute_e.chat_id))
        MONGO.mute_chats.insert_one(
                {"chat_id":mute_e.chat_id}
                )
        await mute_e.edit("`Shush! This chat will be silenced!`")
        if LOGGER:
            await mute_e.client.send_message(
                LOGGER_GROUP,
                str(mute_e.chat_id) + " was silenced.")


@register(incoming=True)
async def keep_read(message):
    """ The mute logic. """
    try:
         from userbot import MONGO
    except AttributeError:
        return
    kread =  MONGO.mute_chats.find(
            {"chat_id":message.chat_id})
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)

HELPER.update({
    'unmutechat': '.unmutechat\
\nUsage: Unmutes a muted chat.'
})

HELPER.update({
    'mutechat': '.mutechat\
\nUsage: Allows you to mute any chat.'
})

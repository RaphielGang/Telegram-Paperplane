# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for muting chats. """

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, MONGO, is_mongo_alive,
                     is_redis_alive)
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.unmutechat$")
@errors_handler
async def unmute_chat(unm_e):
    """ For .unmutechat command, unmute a muted chat. """
    if not unm_e.text[0].isalpha() and unm_e.text[0] not in ("/", "#", "@",
                                                             "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await unm_e.edit("`Database connections failing!`")
            return
        MONGO.bot.mute_chats.delete_one({"chat_id": unm_e.chat_id})
        await unm_e.edit("```Unmuted this chat Successfully```")


@register(outgoing=True, pattern="^.mutechat$")
@errors_handler
async def mute_chat(mute_e):
    """ For .mutechat command, mute any chat. """
    if not mute_e.text[0].isalpha() and mute_e.text[0] not in ("/", "#", "@",
                                                               "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await mute_e.edit("`Database connections failing!`")
            return
        await mute_e.edit(str(mute_e.chat_id))
        MONGO.bot.mute_chats.insert_one({"chat_id": mute_e.chat_id})
        await mute_e.edit("`Shush! This chat will be silenced!`")
        if BOTLOG:
            await mute_e.client.send_message(
                BOTLOG_CHATID,
                str(mute_e.chat_id) + " was silenced.")


@register(incoming=True)
@errors_handler
async def keep_read(message):
    """ The mute logic. """
    if not is_mongo_alive() or not is_redis_alive():
        return
    kread = MONGO.bot.mute_chats.find({"chat_id": message.chat_id})
    if kread:
        for i in kread:
            if i["chat_id"] == message.chat_id:
                await message.client.send_read_acknowledge(message.chat_id)


CMD_HELP.update({'unmutechat': '.unmutechat\
\nUsage: Unmute a muted chat.'})

CMD_HELP.update({'mutechat': '.mutechat\
\nUsage: Mute any chat.'})

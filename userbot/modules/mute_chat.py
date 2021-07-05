# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for muting chats. """

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    MONGO,
    is_mongo_alive,
    is_redis_alive,
)
from userbot.events import register, grp_exclude


@register(outgoing=True, pattern="^.unmutechat$")
@grp_exclude()
async def unmute_chat(unm_e):
    """For .unmutechat command, unmute a muted chat."""
    if not is_mongo_alive() or not is_redis_alive():
        await unm_e.edit("`Database connections failing!`")
        return
    MONGO.bot.mute_chats.delete_one({"chat_id": unm_e.chat_id})
    await unm_e.edit("```Unmuted this chat!```")


@register(outgoing=True, pattern="^.mutechat$")
@grp_exclude()
async def mute_chat(mute_e):
    """For .mutechat command, mute any chat."""
    if not is_mongo_alive() or not is_redis_alive():
        await mute_e.edit("`Database connections failing!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    MONGO.bot.mute_chats.insert_one({"chat_id": mute_e.chat_id})
    await mute_e.edit("`This chat has been muted!`")
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID, str(mute_e.chat_id) + " has been muted."
        )


@register(incoming=True, disable_errors=True)
@grp_exclude()
async def keep_read(message):
    """The mute logic."""
    if not is_mongo_alive() or not is_redis_alive():
        return
    kread = MONGO.bot.mute_chats.find({"chat_id": message.chat_id})
    if kread:
        for i in kread:
            if i["chat_id"] == message.chat_id:
                await message.client.send_read_acknowledge(message.chat_id)


CMD_HELP.update(
    {
        "muting": [
            "Muting",
            " - `.unmutechat`: Unmute a muted chat.\n"
            " - `.mutechat`: Mute any chat.\n",
        ]
    }
)

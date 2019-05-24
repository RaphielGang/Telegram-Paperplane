# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for muting chats. """

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ For .unmutechat command, unmute a muted chat. """
    if not unm_e.text[0].isalpha() and unm_e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.keep_read_sql import unkread
        except AttributeError:
            await unm_e.edit('`Running on Non-SQL Mode!`')
            return
        unkread(str(unm_e.chat_id))
        await unm_e.edit("```Unmuted this chat Successfully```")


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ For .mutechat command, mute any chat. """
    if not mute_e.text[0].isalpha() and mute_e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.keep_read_sql import kread
        except AttributeError:
            await mute_e.edit("`Running on Non-SQL mode!`")
            return
        await mute_e.edit(str(mute_e.chat_id))
        kread(str(mute_e.chat_id))
        await mute_e.edit("`Shush! This chat will be silenced!`")
        if BOTLOG:
            await mute_e.client.send_message(
                BOTLOG_CHATID,
                str(mute_e.chat_id) + " was silenced.")


@register(incoming=True)
async def keep_read(message):
    """ The mute logic. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)

CMD_HELP.update({
    'unmutechat': '.unmutechat\
\nUsage: Unmutes a muted chat.'
})

CMD_HELP.update({
    'mutechat': '.mutechat\
\nUsage: Allows you to mute any chat.'
})

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import time

from telethon.events import StopPropagation

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, COUNT_MSG, USERS,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import afk, afk_reason, is_afk, no_afk


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the
     people who mention you that you are AFK."""

    global COUNT_MSG
    global USERS
    if not is_redis_alive():
        return
    IsAway = await is_afk()
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if IsAway is True:
            if mention.sender_id not in USERS:
                await mention.reply(
                    "Sorry! My boss is AFK due to " + await afk_reason() +
                    ". Would ping him to look into the message soon😉")
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % 5 == 0:
                    await mention.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```" +
                        await afk_reason() + "```")
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(afk_pm):
    global USERS
    global COUNT_MSG
    if not is_redis_alive():
        return
    IsAway = await is_afk()
    if afk_pm.is_private and not (await afk_pm.get_sender()).bot:
        if IsAway is True:
            if afk_pm.sender_id not in USERS:
                await afk_pm.reply(
                    "Sorry! My boss is AFK due to ```" + await afk_reason() +
                    "``` I'll ping him to look into the message soon😉")
                USERS.update({afk_pm.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif afk_pm.sender_id in USERS:
                if USERS[afk_pm.sender_id] % 5 == 0:
                    await afk_pm.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```" +
                        await afk_reason() + "```")
                    USERS[afk_pm.sender_id] = USERS[afk_pm.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[afk_pm.sender_id] = USERS[afk_pm.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, disable_errors=True, pattern="^.afk")
async def set_afk(setafk):
    if not is_redis_alive():
        await setafk.edit("`Database connections failing!`")
        return
    message = setafk.text
    try:
        AFKREASON = str(message[5:])
    except BaseException:
        AFKREASON = ''
    if not AFKREASON:
        AFKREASON = 'No reason'
    await setafk.edit("AFK AF!")
    if BOTLOG:
        await setafk.client.send_message(BOTLOG_CHATID, "You went AFK!")
    await afk(AFKREASON)
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    global COUNT_MSG
    global USERS
    if not is_redis_alive():
        return
    IsAway = await is_afk()
    if IsAway is True:
        x = await notafk.respond("I'm no longer AFK.")
        y = await notafk.respond(
            "`You recieved " + str(COUNT_MSG) +
            " messages while you were away. Check log for more details.`" +
            " `This auto-generated message " +
            "shall be self destructed in 2 seconds.`")
        await no_afk()
        time.sleep(2)
        await x.delete()
        await y.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved " + str(COUNT_MSG) + " messages from " +
                str(len(USERS)) + " chats while you were away",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " sent you " + "`" + str(USERS[i]) + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}


CMD_HELP.update({
    "afk":
    ".afk <reason>(optional)"
    "\nUsage: Sets your status as AFK. Responds to anyone who tags/PM's "
    "you telling you are AFK. Switches off AFK when you type back anything."
})

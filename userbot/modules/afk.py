# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import time

from telethon.events import StopPropagation

from userbot import (COUNT_MSG, REDIS, BOTLOG, BOTLOG_CHATID, USERS, CMD_HELP, REDIS, is_redis_alive)
from userbot.events import register


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    if not is_redis_alive():
        return
    AFK = REDIS.get('isafk')
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if AFK:
            if mention.sender_id not in USERS:
                print(str(AFK))
                await mention.reply(
                    "Sorry! My boss is AFK due to "
                    + AFK
                    + ". Would ping him to look into the message soon😉"
                )
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % 5 == 0:
                    await mention.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```"
                        + AFK
                        + "```"
                    )
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True)
async def afk_on_pm(e):
    global USERS
    global COUNT_MSG
    if not is_redis_alive():
        return
    AFK = REDIS.get('isafk')
    if e.is_private and not (await e.get_sender()).bot:
        if AFK:
            if e.sender_id not in USERS:
                await e.reply(
                    "Sorry! My boss is AFK due to ```"
                    + AFK
                    + "``` I'll ping him to look into the message soon😉"
                )
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif e.sender_id in USERS:
                if USERS[e.sender_id] % 5 == 0:
                    await e.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```"
                        + AFK
                        + "```"
                    )
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk")
async def set_afk(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if not is_redis_alive():
            await e.edit("`Database connections failing!`")
            return
        message = e.text
        try:
            AFKREASON = str(message[5:])
        except:
            AFKREASON = ''
        if not AFKREASON:
            AFKREASON = 'No reason'
        await e.edit("AFK AF!")
        if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "You went AFK!")
        REDIS.set('isafk', AFKREASON)
        AFK = REDIS.get('isafk')
        print(str(AFK))
        raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(e):
    global COUNT_MSG
    global USERS
    global AFKREASON
    if is_redis_alive():
        return
    ISAFK = REDIS.get('isafk')
    if ISAFK:
        REDIS.delete('isafk')
        await e.respond("I'm no longer AFK.")
        x = await e.respond(
            "`You recieved "
            + str(COUNT_MSG)
            + " messages while you were away. Check log for more details.`"
            + " `This auto-generated message shall be self destructed in 2 seconds.`"
        )
        time.sleep(2)
        await afk_info.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved " +
                str(COUNT_MSG) +
                " messages from " +
                str(len(USERS)) +
                " chats while you were away",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" +
                    name0 +
                    "](tg://user?id=" +
                    str(i) +
                    ")" +
                    " sent you " +
                    "`" +
                    str(USERS[i]) +
                    " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = "No Reason"

CMD_HELP.update({
    "afk": ".afk <reason>(reason is optional)\
\nUsage: Sets you as afk. Responds to anyone who tags/PM's \
you telling that you are afk. Switches off AFK when you type back anything.\
"
})

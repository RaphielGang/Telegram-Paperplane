# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

import time

from telethon.events import StopPropagation

from userbot import (COUNT_MSG, REDIS, LOGGER, LOGGER_GROUP, USERS, HELPER)
from userbot.events import register


@register(incoming=True)
async def mention_afk(e):
    global COUNT_MSG
    global USERS
    AFK = REDIS.get('isafk')
    if e.message.mentioned and not (await e.get_sender()).bot:
        if AFK:
            if e.sender_id not in USERS:
                print(str(AFK))
                await e.reply(
                    "Sorry! My boss is AFK due to "
                    + AFK
                    + ". Would ping him to look into the message soon😉"
                )
                USERS.update({e.sender_id: 1})
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
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True)
async def afk_on_pm(e):
    global USERS
    global COUNT_MSG
    AFK = REDIS.get('isafk')
    if e.is_private and not (await e.get_sender()).bot:
        if AFK:
            if e.sender_id not in USERS:
                await e.reply(
                    "Sorry! My boss is AFK due to ```"
                    + AFK
                    + "``` I'll ping him to look into the message soon😉"
                )
                USERS.update({e.sender_id: 1})
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
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk")
async def set_afk(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        try:
            AFKREASON = str(message[5:])
        except:
            AFKREASON = ''
        if not AFKREASON:
            AFKREASON = 'No reason'
        await e.edit("AFK AF!")
        if LOGGER:
            await e.client.send_message(LOGGER_GROUP, "You went AFK!")
        REDIS.set('isafk', AFKREASON)
        AFK = REDIS.get('isafk')
        print(str(AFK))
        raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(e):
    global COUNT_MSG
    global USERS
    global AFKREASON
    ISAFK = REDIS.get('isafk')
    if ISAFK:
        REDIS.delete('isafk')
        await e.respond("I'm no longer AFK.")
        x = await e.respond(
            "`You recieved "
            + str(COUNT_MSG)
            + " messages while you were away. Check log for more details.`"
            + "`This auto-generated message shall be self destructed in 2 seconds.`"
        )
        time.sleep(2)
        await x.delete()
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "You've recieved "
                + str(COUNT_MSG)
                + " messages from "
                + str(len(USERS))
                + " chats while you were away",
            )
            for i in USERS:
                name = await e.client.get_entity(i)
                name0 = str(name.first_name)
                await e.client.send_message(
                    LOGGER_GROUP,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " sent you "
                    + "`"
                    + str(USERS[i])
                    + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = "No Reason"

HELPER.update({
    "afk": "Usage: \nSets you as afk. Responds to anyone who tags/PM's you telling that you are afk. Switches off AFK when you type back anything."
})

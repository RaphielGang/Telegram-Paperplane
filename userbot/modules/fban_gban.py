# Copyright (C) 2019 Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from userbot import bot, CMD_HELP, is_mongo_alive, is_redis_alive
from userbot.events import register, errors_handler
from telethon.tl.types import MessageEntityMentionName
from userbot.modules.dbhelper import get_fban, add_chat_fban, remove_chat_fban, get_gban, add_chat_gban, remove_chat_gban
import asyncio


@register(outgoing=True, pattern="^.gban")
@errors_handler
async def gban_all(msg):
    if not msg.text[0].isalpha() and msg.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await msg.edit("`Database connections failing!`")
            return
        textx = await msg.get_reply_message()
        if textx:
            try:
                banreason = "[userbot] "
                banreason += banreason.join(msg.text.split(" ")[1:])
                if banreason == "[userbot]":
                    raise TypeError
            except TypeError:
                banreason = "[userbot] gban"
        else:
            banid = msg.text.split(" ")[1]
            if banid.isnumeric():
                # if its a user id
                banid = int(banid)
            else:
                # deal wid the usernames
                if msg.message.entities is not None:
                    probable_user_mention_entity = msg.message.entities[0]

                if isinstance(probable_user_mention_entity,
                              MessageEntityMentionName):
                    ban_id = probable_user_mention_entity.user_id
            try:
                banreason = "[userbot] "
                banreason += banreason.join(msg.text.split(" ")[2:])
                if banreason == "[userbot]":
                    raise TypeError
            except TypeError:
                banreason = "[userbot] fban"
        if not textx:
            await msg.edit(
                "Reply Message missing! Might fail on many bots! Still attempting Gban!"
            )
            # Ensure User Read the warning
            await asyncio.sleep(1)
        x = (await get_gban())
        count = 0
        banlist = []
        for i in x:
            banlist.append(i["chatid"])
        for banbot in banlist:
            async with bot.conversation(banbot) as conv:
                if textx:
                    c = await msg.forward_to(banbot)
                    await c.reply("/id")
                await conv.send_message(f"/gban {banid} {banreason}")
                resp = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                count += 1
                # We cant see if he actually Gbanned. Let this stay for now
                await msg.edit("`Gbanned on " + str(count) + " bots!`")
                await asyncio.sleep(0.2)


@register(outgoing=True, pattern="^.fban")
@errors_handler
async def fedban_all(msg):
    if not msg.text[0].isalpha() and msg.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await msg.edit("`Database connections failing!`")
            return
        textx = await msg.get_reply_message()
        if textx:
            try:
                banreason = "[userbot] "
                banreason += banreason.join(msg.text.split(" ")[1:])
                if banreason == "[userbot]":
                    raise TypeError
            except TypeError:
                banreason = "[userbot] fban"
        else:
            banid = msg.text.split(" ")[1]
            if banid.isnumeric():
                # if its a user id
                banid = int(banid)
            else:
                # deal wid the usernames
                if msg.message.entities is not None:
                    probable_user_mention_entity = msg.message.entities[0]

                if isinstance(probable_user_mention_entity,
                              MessageEntityMentionName):
                    ban_id = probable_user_mention_entity.user_id
            try:
                banreason = "[userbot] "
                banreason += banreason.join(msg.text.split(" ")[2:])
                if banreason == "[userbot]":
                    raise TypeError
            except TypeError:
                banreason = "[userbot] fban"
            if "spam" in banreason:
                spamwatch = True
            else:
                spamwatch = False
        failed = dict()
        count = 1
        fbanlist = []
        x = (await get_fban())
        for i in x:
            fbanlist.append(i["chatid"])
        for bangroup in fbanlist:

            # Send to proof to Spamwatch in case it was spam
            # Spamwatch is a reputed fed fighting against spam on telegram

            if bangroup == -1001312712379:
                if spamwatch:
                    if textx:
                        await textx.forward_to(-1001312712379)
                        # Tag him, coz we can't fban xd
                        await bot.send_message(-1001312712379, "@SitiSchu")
                    else:
                        await msg.reply(
                            "`Spam message detected. But no reply message, can't forward to spamwatch`"
                        )
                continue
            async with bot.conversation(bangroup) as conv:
                await conv.send_message(f"!fban {banid} {banreason}")
                resp = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                if "Beginning federation ban " not in resp.text:
                    failed[bangroup] = str(conv.chat_id)
                else:
                    count += 1
                    await msg.edit("`Fbanned on " + str(count) + " feds!`")
                # Sleep to avoid a floodwait.
                # Prevents floodwait if user is a fedadmin on too many feds
                await asyncio.sleep(0.2)
        if failed:
            failedstr = ""
            for i in failed.keys():
                failedstr += failed[i]
                failedstr += " "
            await msg.reply(f"`Failed to fban in {failedstr}`")
        else:
            await msg.reply("`Fbanned in all feds!`")


@register(outgoing=True, pattern="^.addfban")
@errors_handler
async def add_to_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await add_chat_fban(chat.chat_id)
    await chat.edit("`Added this chat under the Fbanlist!`")


@register(outgoing=True, pattern="^.addgban")
@errors_handler
async def add_to_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await add_chat_gban(chat.chat_id)
    print(chat.chat_id)
    await chat.edit("`Added this bot under the Gbanlist!`")


@register(outgoing=True, pattern="^.removefban")
@errors_handler
async def remove_from_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await remove_chat_fban(chat.chat_id)
    await chat.edit("`Removed this chat from the Fbanlist!`")


@register(outgoing=True, pattern="^.removegban")
@errors_handler
async def remove_from_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await remove_chat_gban(chat.chat_id)
    await chat.edit("`Removed this bot from the Gbanlist!`")


CMD_HELP.update({
    "gbanall":
    """.gban\n
Usage: Reply to a user to ban them in all the bots provided by you!""",
    "fbanall":
    """.fban\n
Usage: Reply to a user to fban them in all the groups provided by you!"""
})

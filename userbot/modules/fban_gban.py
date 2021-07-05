# Copyright (C) 2019 Rupansh Sekar.
# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio

from telethon.tl.types import MessageEntityMentionName

from userbot import CMD_HELP, bot, is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude
from userbot.modules.dbhelper import (
    add_chat_fban,
    add_chat_gban,
    get_fban,
    get_gban,
    remove_chat_fban,
    remove_chat_gban,
)


@register(outgoing=True, pattern="^.gban")
@grp_exclude()
async def gban_all(msg):
    if not is_mongo_alive() or not is_redis_alive():
        await msg.edit("`Database connections failing!`")
        return
    textx = await msg.get_reply_message()
    if textx:
        try:
            banreason = banreason.join(msg.text.split(" ")[1:])
        except TypeError:
            banreason = "[paperplane] GBan"
    else:
        banid = msg.text.split(" ")[1]
        if banid.isnumeric():
            # if its a user id
            banid = int(banid)
        else:
            # deal wid the usernames
            if msg.message.entities is not None:
                probable_user_mention_entity = msg.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                banid = probable_user_mention_entity.user_id
        try:
            banreason = banreason.join(msg.text.split(" ")[2:])
        except TypeError:
            banreason = "[paperplane] GBan"
    if not textx:
        await msg.edit(
            "Reply message missing! Might fail on many bots! Still attempting to Gban!"
        )
        # Ensure User Read the warning
        await asyncio.sleep(1)
    x = await get_gban()
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
            await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            count += 1
            # We cant see if he actually Gbanned. Let this stay for now
            await msg.edit("`Gbanned on " + str(count) + " bots!`")
            await asyncio.sleep(0.2)


@register(outgoing=True, pattern="^.fban")
@grp_exclude()
async def fedban_all(msg):
    if not is_mongo_alive() or not is_redis_alive():
        await msg.edit("`Database connections failing!`")
        return
    textx = await msg.get_reply_message()
    if textx:
        try:
            banreason = banreason.join(msg.text.split(" ")[1:])
        except TypeError:
            banreason = "[paperplane] FBan"
    else:
        banid = msg.text.split(" ")[1]
        if banid.isnumeric():
            # if its a user id
            banid = int(banid)
        else:
            # deal wid the usernames
            if msg.message.entities is not None:
                probable_user_mention_entity = msg.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                banid = probable_user_mention_entity.user_id
        try:
            banreason = banreason.join(msg.text.split(" ")[2:])
        except TypeError:
            banreason = "[paperplane] FBan"
    failed = {}
    count = 1
    fbanlist = []
    x = await get_fban()
    for i in x:
        fbanlist.append(i["chatid"])
    for bangroup in fbanlist:
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
        for i in failed.values():
            failedstr += i
            failedstr += " "
        await msg.reply(f"`Failed to fban in {failedstr}`")
    else:
        await msg.reply("`Fbanned in all feds!`")


@register(outgoing=True, pattern="^.addfban")
@grp_exclude()
async def add_to_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await add_chat_fban(chat.chat_id)
    await chat.edit("`Added this chat under the Fbanlist!`")


@register(outgoing=True, pattern="^.addgban")
@grp_exclude()
async def add_to_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await add_chat_gban(chat.chat_id)
    print(chat.chat_id)
    await chat.edit("`Added this bot under the Gbanlist!`")


@register(outgoing=True, pattern="^.removefban")
@grp_exclude()
async def remove_from_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await remove_chat_fban(chat.chat_id)
    await chat.edit("`Removed this chat from the Fbanlist!`")


@register(outgoing=True, pattern="^.removegban")
@grp_exclude()
async def remove_from_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await remove_chat_gban(chat.chat_id)
    await chat.edit("`Removed this bot from the Gbanlist!`")


CMD_HELP.update(
    {
        "fbans/gbans": [
            "FBans/GBans",
            " - `.gban`: Reply to a user to ban them in all the bots provided by you.\n"
            " - `.fban`: Reply to a user to fban them in all the groups provided by you.\n"
            " - `.addfban`: Add this group to the fbanlist.\n"
            " - `.addgban`: Add this group to the gbanlist.\n"
            " - `.removefban`: Remove this group from the fbanlist.\n"
            " - `.removegban`: Remove this group from the gbanlist.\n",
        ]
    }
)

# Copyright (C) 2019 Rupansh Sekar.
# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio

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
from userbot.modules import helpers


@register(outgoing=True, pattern="^.gban(?: |$)([^\s]+)(?: |$)(.*)")
@grp_exclude()
async def gban_all(msg):
    if not is_mongo_alive() or not is_redis_alive():
        await msg.edit("`Database connections failing!`")
        return
    banreason = "[paperplane] "

    user, reason = await helpers.get_user_and_reason_from_event(msg)
    if not user:
        await msg.edit(
            "`Missing user to GBan! Either reply to message, mention the user or specify a valid ID!`"
        )
        return
    banid = user.id
    banreason += reason if reason else "GBan"
    message = ""

    textx = await msg.get_reply_message()
    if not textx:
        message += "`Reply message missing! Might fail on some bots! Still attempting to GBan!`"
        await msg.edit(message)

    banlist = await get_gban()
    count = 0
    banid_list = [row["chatid"] for row in banlist]
    for banbot in banid_list:
        async with bot.conversation(banbot) as conv:
            if textx:
                await msg.forward_to(banbot)
            await conv.send_message(f"/gban {banid} {banreason}")
            count += 1

    # We can't see if the user is actually Gbanned.
    message = f"\n`Gbanned on {str(count)} bot(s)! Paperplane doesn't check if the GBans were successful.`"
    await msg.edit(message)


@register(outgoing=True, pattern="^.fban(?: |$)([^\s]+)(?: |$)(.*)")
@grp_exclude()
async def fedban_all(msg):
    if not is_mongo_alive() or not is_redis_alive():
        await msg.edit("`Database connections failing!`")
        return

    banreason = "[paperplane] "

    user, reason = await helpers.get_user_and_reason_from_event(msg)
    if not user:
        await msg.edit(
            "`Missing user to FBan! Either reply to message, mention the user or specify a valid ID!`"
        )
        return
    banid = user.id
    banreason += reason if reason else "FBan"
    message = ""

    textx = await msg.get_reply_message()
    if not textx:
        message += "`Reply message missing! Might fail on some bots! Still attempting to FBan!`"
        await msg.edit(message)

    banlist = await get_fban()
    count = 0
    banid_list = [row["chatid"] for row in banlist]
    for bangroup in banid_list:
        async with bot.conversation(bangroup) as conv:
            await conv.send_message(f"!fban {banid} {banreason}")
            count += 1
            # Sleep to avoid a floodwait.
            # Prevents floodwait if user is a fedadmin on too many feds
            await asyncio.sleep(0.1)

    # We can't see if the user is actually FBanned.
    message = f"\n`Fbanned on {str(count)} fed(s)! Paperplane doesn't check if the FBans were successful.`"
    await msg.edit(message)


@register(outgoing=True, pattern="^.addfban")
@grp_exclude()
async def add_to_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    res = await add_chat_fban(chat.chat_id)

    if res:
        return await chat.edit("`Added this chat to the FBan list!`")
    else:
        return await chat.edit(
            "`Couldn't add this chat to the FBan list! Maybe it's already there?`"
        )


@register(outgoing=True, pattern="^.addgban")
@grp_exclude()
async def add_to_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    res = await add_chat_gban(chat.chat_id)

    if res:
        return await chat.edit("`Added this bot to the GBan list!`")
    else:
        return await chat.edit(
            "`Couldn't add this bot to the GBan list! Maybe it's already there?`"
        )


@register(outgoing=True, pattern="^.removefban")
@grp_exclude()
async def remove_from_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    res = await remove_chat_fban(chat.chat_id)

    if res:
        return await chat.edit("`Removed this group from the FBan list!`")
    else:
        return await chat.edit(
            "`Couldn't remove this group from the FBan list! Maybe it's not there?`"
        )


@register(outgoing=True, pattern="^.removegban")
@grp_exclude()
async def remove_from_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    res = await remove_chat_gban(chat.chat_id)

    if res:
        return await chat.edit("`Removed this bot from the GBan list!`")
    else:
        return await chat.edit(
            "`Couldn't remove this bot from the GBan list! Maybe it's not there?`"
        )


@register(outgoing=True, pattern="^.listfban")
@grp_exclude()
async def list_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    banlist = await get_fban()
    id_list = [row["chatid"] for row in banlist]
    if not id_list:
        return await chat.edit(
            "`No groups in the FBan list! Add some with the` `.addfban` `command!`"
        )
    message = "`Paperplane FBan groups`\n"

    for id in id_list:
        message += f"`* {id}`\n"

    await chat.edit(message)


@register(outgoing=True, pattern="^.listgban")
@grp_exclude()
async def list_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    banlist = await get_fban()
    id_list = [row["chatid"] for row in banlist]
    if not id_list:
        return await chat.edit(
            "`No bots in the GBan list! Add some with the` `.addgban` `command!`"
        )
    message = "`Paperplane GBan bots`\n"

    for id in id_list:
        message += f"`* {id}`\n"

    await chat.edit(message)


CMD_HELP.update(
    {
        "fbans/gbans": [
            "FBans/GBans",
            " - `.gban`: Reply to a user to GBan them in all the bots provided by you.\n"
            " - `.fban`: Reply to a user to FBan them in all the groups provided by you.\n"
            " - `.addfban`: Add this group to the FBanlist.\n"
            " - `.addgban`: Add this bot to the GBanlist.\n"
            " - `.removefban`: Remove this group from the FBanlist.\n"
            " - `.removegban`: Remove this bot from the GBanlist.\n",
            " - `.listfban`: List all groups in the FBan list.\n",
            " - `.listgban`: List all bots in the GBan list.\n",
        ]
    }
)

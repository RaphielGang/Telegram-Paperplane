# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for keeping control on who can PM you. """

import asyncio

from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User

from userbot import (
    MONGO,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    COUNT_PM,
    LASTMSG,
    LOGS,
    PM_AUTO_BAN,
    MAX_FLOOD_IN_PM,
    is_mongo_alive,
    is_redis_alive,
    #PM_PERMIT_IMAGE,
    PM_PERMIT_MSG,
    
)
from userbot.events import register, grp_exclude
from userbot.modules.dbhelper import (
    autoapproval,
    autoapprove,
    approval,
    approve,
    disapprove,
    block_pm,
    notif_off,
    notif_on,
    notif_state,
)

# ========================= CONSTANTS ============================
UNAPPROVED_MSG = PM_PERMIT_MSG or (
    "Bleep blop! I am a bot. Hmm... I don't remember seeing you around.\n\n"
    "So I will wait for my owner to look in and approve you. "
    "They mostly approve PMs.\n\n"
    "**Till then, don't try to spam! Follow my warnings or I will block you!!**"
)

MAX_MSG = MAX_FLOOD_IN_PM or 5
PM_PERMIT_IMAGE=""
# =================================================================

async def del_in(text, seconds):
    await asyncio.sleep(seconds)
    return await text.delete()


@register(incoming=True, disable_edited=True, disable_errors=True)
@grp_exclude()
async def permitpm(event):
    """ Permits people from PMing you without approval. \
        Will block retarded nibbas automatically. """
    if PM_AUTO_BAN:
        if event.is_private and not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return
            if await approval(event.chat_id) is False:
                if MONGO.userbot.pmpermit.find_one({'prev_msg': event.chat_id}) is None:
                    if PM_PERMIT_IMAGE:
                        x = await event.respond(UNAPPROVED_MSG, file=PM_PERMIT_IMAGE)
                        MONGO.userbot.pmpermit.insert_one({'prev_msg': event.chat_id})
                    elif not PM_PERMIT_IMAGE:
                        y = await event.respond(UNAPPROVED_MSG)
                        MONGO.userbot.pmpermit.insert_one({'prev_msg': event.chat_id})
                else:
                    y.delete()
                            

                        
    
    
@register(outgoing=True, pattern="^.autoapprove$|^.autoa$")
@grp_exclude()
async def auto_approve_switch(event):
    """Will switch auto approve on or off"""
    if not is_mongo_alive() or not is_redis_alive():
        await apprvpm.edit("`Database connections failing!`")
        return
    else:
        chat = await event.get_chat()
        await autoapprove(chat.id)
        if await autoapproval(event.chat_id) is True:
            x = await event.edit("`Auto-Approve` ON! I will approve an user after you PM them.")
            await del_in(x, 5)
        else:
            y = await event.edit("`Auto-Approve` OFF! You will have to manually approve users now.")
            await del_in(y, 5)
    
    
@register(disable_edited=True, outgoing=True, disable_errors=True)
@grp_exclude()
async def auto_accept(event):
    """Will approve automatically if you texted them first."""
    if await autoapproval(event.chat_id) is True:
        chat = await event.get_chat()
        if not is_mongo_alive() or not is_redis_alive():
            return
        if event.text.startswith((".block", ".autoa", ".a", ".da", ".autoapprove", ".approve", ".disapprove", ".notifon", ".notifoff")):
            return
        if event.is_private and not await approval(event.chat_id) and not chat.bot:
            await approve(chat.id)
            async for message in apprvpm.client.iter_messages(apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG):
                await message.delete()
            try:
                del COUNT_PM[apprvpm.chat_id]
                del LASTMSG[apprvpm.chat_id]
            except KeyError:
                if BOTLOG:
                    await event.client.send_message(BOTLOG_CHATID, "PMPermit broke, please restart Paperplane.")
                    LOGS.info("PMPermit broke, please restart Paperplane.")
                    return
            if BOTLOG:
                await event.client.send_message(
                BOTLOG_CHATID,
                "#AUTO-APPROVED\n"
                + "User: "
                + f"[{chat.first_name}](tg://user?id={chat.id})",
          )


@register(outgoing=True, pattern="^.notifoff$")
@grp_exclude()
async def notifoff(noff_event):
    """For .notifoff command, stop getting
    notifications from unapproved PMs."""
    if await notif_off() is False:
        x = await noff_event.edit("`Notifications are already silenced!`")
        return await del_in(x, 5)
    else:
        y = await noff_event.edit("`Notifications silenced!`")
        return await del_in(y, 5)  
 

@register(outgoing=True, pattern="^.notifon$")
@grp_exclude()
async def notifon(non_event):
    """For .notifoff command, get notifications from unapproved PMs."""
    if await notif_on() is False:
        x = await non_event.edit("`Notifications aren't muted!")
        return await del_in(x, 5)
    else:
        y = await non_event.edit("`Notifications unmuted!`")
        return await del_in(y, 5)

@register(outgoing=True, pattern="^.approve$|^.a$")
@grp_exclude()
async def approvepm(apprvpm):
    """For .approve command, give someone the permissions to PM you."""
    if not is_mongo_alive() or not is_redis_alive():
        await apprvpm.edit("`Database connections failing!`")
        return
    
    chat = await apprvpm.get_chat()
    if await approve(apprvpm.chat_id) is False:
        x = await apprvpm.edit("`I already know this user! You can chat!`")
        return await del_in(x, 5)
        
    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        replied_user = await apprvpm.client(GetFullUserRequest(reply.from_id))
        aname = replied_user.user.id
        name0 = str(replied_user.user.first_name)
        uid = replied_user.user.id

    else:
        aname = await apprvpm.client.get_entity(apprvpm.chat_id)
        name0 = str(aname.first_name)
        uid = apprvpm.chat_id
        
    await approve(chat.id)
    await apprvpm.edit(f"I will remember [{name0}](tg://user?id={uid}) as your __mutual__ contact😉")
    await asyncio.sleep(3)
    async for message in apprvpm.client.iter_messages(
        apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG):
        await message.delete()
    await apprvpm.edit("Hey there! Nice to meet you☺ I am an obidient bot of my owner!")
    
    try:
        del COUNT_PM[apprvpm.chat_id]
        del LASTMSG[apprvpm.chat_id]
    except KeyError:
        if BOTLOG:
           await apprvpm.client.send_message(BOTLOG_CHATID, "PMPermit broke, please restart Paperplane.")
           LOGS.info("PMPermit broke, please restart Paperplane.")
           return
  
    if BOTLOG:
        await apprvpm.client.send_message(
            BOTLOG_CHATID, "#APPROVED\n" + "User: " + f"[{name0}](tg://user?id={uid})"
        )

@register(outgoing=True, pattern="^.disapprove$|^.da$")
@grp_exclude()
async def dapprovepm(dapprvpm):
    """For .disapprove command, revokes someone's permission to PM you."""
    if not is_mongo_alive() or not is_redis_alive():
        await dapprvpm.edit("`Database connections failing!`")
        return

    chat = await dapprvpm.get_chat()
    if await approve(dapprvpm.chat_id) is True:
        x = await dapprvpm.edit("`I don't remember approving this user!`")
        return await del_in(x, 5)
        
    if dapprvpm.reply_to_msg_id:
        reply = await dapprvpm.get_reply_message()
        replied_user = await dapprvpm.client(GetFullUserRequest(reply.from_id))
        aname = replied_user.user.id
        name0 = str(replied_user.user.first_name)
        uid = replied_user.user.id

    else:
        aname = await dapprvpm.client.get_entity(dapprvpm.chat_id)
        name0 = str(aname.first_name)
        uid = dapprvpm.chat_id
    
    await disapprove(chat.id)
    await dapprvpm.edit(f"Forgetting [{name0}](tg://user?id={uid}) .")
    await asyncio.sleep(1)
    await dapprvpm.edit(f"Forgetting [{name0}](tg://user?id={uid}) ..")
    await asyncio.sleep(1)
    await dapprvpm.edit(f"Forgetting [{name0}](tg://user?id={uid}) ...")
    await asyncio.sleep(1)
    await dapprvpm.edit(f"Forgetting [{name0}](tg://user?id={uid}) ... Done!")
    await asyncio.sleep(1)
    if dapprvpm.is_private:
        await dapprvpm.edit("I don't like strangers in the PM!! Get lost!")
    else:
        await dapprvpm.edit("Don't you dare PM!!")

    if BOTLOG:
        await dapprvpm.client.send_message(
            BOTLOG_CHATID, "#DISAPPROVED\n" + "User: " + f"[{name0}](tg://user?id={uid})"
        )
        
        
        
@register(outgoing=True, pattern="^.block$")
@grp_exclude()
async def blockpm(block):
    """For .block command, block people from PMing you!"""
    if not is_mongo_alive() or not is_redis_alive():
        await block.edit("`Database connections failing!`")
        return

    if await block_pm(block.chat_id) is False:
        x = await block.edit("`The user isn't approved.`")
        return await del_in(x, 5)
    else:    
        y = await block.edit("`You are gonna be blocked from PM-ing my owner!`")
        await asyncio.sleep(2)
        
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client(GetFullUserRequest(reply.from_id))
        aname = replied_user.user.id
        name0 = str(replied_user.user.first_name)
        await block.client(BlockRequest(replied_user.user.id))
        uid = replied_user.user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        name0 = str(aname.first_name)
        uid = block.chat_id

    await block.edit("**Blocked.**")

    if BOTLOG:
        await block.client.send_message(
            BOTLOG_CHATID, "#BLOCKED\n" + "User: " + f"[{name0}](tg://user?id={uid})"
        )


@register(outgoing=True, pattern="^.unblock$")
@grp_exclude()
async def unblockpm(unblock):
    """For .unblock command, let people PMing you again!"""
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client(GetFullUserRequest(reply.from_id))
        name0 = str(replied_user.user.first_name)
        if await approve(reply.from_id) is False:
            x = await unblock.edit("`You haven't blocked this user yet!`")
            return await del_in(x, 5)

        await unblock.client(UnblockRequest(replied_user.user.id))
        await unblock.edit("`My owner has unblocked you. You can PM them now.`")
        

    if BOTLOG:
        await unblock.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={replied_user.user.id})" " was unblocked!.",
        )


CMD_HELP.update(
    {
        "pmpermit": [
            "PMPermit",
            " - `.autoapprove`|`.autoa`: Switches Auto-Approve module on/off.\n"
            " - `.approve`|`.a`: Approve the mentioned/replied person to PM.\n"
            " - `.disapprove`|`.da`: Disapprove the mentioned/replied person to PM.\n"
            " - `.block`: Blocks the person from PMing you.\n"
            " - `.unblock`: Unblocks the person, so they can PM you again.\n"
            " - `.notifoff`: Stop any notifications coming from unapproved PMs.\n"
            " - `.notifon`: Allow notifications coming from unapproved PMs.\n",
        ]
    }
)

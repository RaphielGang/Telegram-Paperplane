# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for keeping control on who can PM you. """

import time
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, COUNT_PM, LASTMSG, LOGS,
                     PM_AUTO_BAN, MAX_FLOOD_IN_PM, PM_PERMIT_MSG, PM_PERMIT_IMAGE, is_mongo_alive, is_redis_alive)
from userbot.events import register, grp_exclude
from userbot.modules.dbhelper import (approval, disapprove, approve, block_pm, notif_off,
                                      notif_on, notif_state)

# ========================= CONSTANTS ============================
#1
UNAPPROVED_MSG = PM_PERMIT_MSG or (
                        "**Bleep blop! I am a bot.**\n\n"
                        "`My master hasn't approved you to PM. `"
                        "`Please wait for my master to look in, he mostly approves PMs.\n\n`"
                        "**So please don't spam here. Otherwise you will be blocked.**")
#2
MAX_MSG = MAX_FLOOD_IN_PM or 4

#3
PP_PM_PIC = PM_PERMIT_IMAGE
# =================================================================


@register(incoming=True, disable_edited=True, disable_errors=True)
@grp_exclude()
async def permitpm(event):
    """ Permits people from PMing you without approval. \
        Will block retarded nibbas automatically. """
    if PM_AUTO_BAN:
        if event.is_private and not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return
            apprv = await approval(event.chat_id)

            # This part basically is a sanity check
            # If the message that sent before is Unapproved Message
            # then stop sending it again to prevent FloodHit
            if not apprv and event.text != UNAPPROVED_MSG:
                if event.chat_id in LASTMSG:
                    prevmsg = LASTMSG[event.chat_id]
                    # If the message doesn't same as previous one
                    # Send the Unapproved Message again
                    if event.text != prevmsg:
                        # Searches for previously sent UNAPPROVED_MSGs
                        async for message in event.client.iter_messages(
                                event.chat_id,
                                from_user='me',
                                search=UNAPPROVED_MSG):
                            # ... and deletes them !!
                            await message.delete()
                        #await event.reply(UNAPPROVED_MSG) 
                        # ignore this please
                    LASTMSG.update({event.chat_id: event.text})
                else:
                    if PM_PERMIT_IMAGE:
                       r = await event.client.send_file(
                                          event.chat_id,
                                          PP_PM_PIC,
                                          caption=UNAPPROVED_MSG,
                                  )
                       LASTMSG.update({event.chat_id: event.text})
                    else:
                       await event.reply(UNAPPROVED_MSG)
                       LASTMSG.update({event.chat_id: event.text})

                if await notif_state() is False:
                    await event.client.send_read_acknowledge(event.chat_id)
                if event.chat_id not in COUNT_PM:
                    COUNT_PM.update({event.chat_id: 1})
                else:
                    COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1
                    
                if COUNT_PM[event.chat_id] < MAX_MSG - 1:
                    #await r.delete
                    WARNS = MAX_MSG - COUNT_PM[event.chat_id]
                    s = await event.reply(f"You have {WARNS} warns left.")
                    
                if MAX_MSG - COUNT_PM[event.chat_id] == 1:
                    #await s.delete
                    t = await event.reply("You have 1 warn left.")
                    
                if COUNT_PM[event.chat_id] == MAX_MSG:
                    #await t.delete()
                    await event.reply("It's the last warning. I will block")

                if COUNT_PM[event.chat_id] > MAX_MSG:
                    message = event.text
                    count = int(message[9:])
                    i = 1

                    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
                        if i > count + 1:
                           break
                        i += 1
                    await message.delete()
                    await event.respond("`You were spamming my master's PM, "
                                        " which I don't like.`"
                                        " `I'mma Report Spam.`")
                      

                    try:
                        del COUNT_PM[event.chat_id]
                        del LASTMSG[event.chat_id]
                    except KeyError:
                        if BOTLOG:
                            await event.client.send_message(
                                BOTLOG_CHATID,
                                "Count PM is seemingly going retard, "
                                "plis restart bot!",
                            )
                        LOGS.info("CountPM wen't rarted boi")
                        return

                    await event.client(BlockRequest(event.chat_id))
                    await event.client(ReportSpamRequest(peer=event.chat_id)) 
                    

                    if BOTLOG:
                        name = await event.client.get_entity(event.chat_id)
                        name0 = str(name.first_name)
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "[" + name0 + "](tg://user?id=" +
                            str(event.chat_id) + ")" +
                            " was just another retard.",
                        )


#Ignore this please
#@register(disable_edited=True, outgoing=True, disable_errors=True)
#@grp_exclude()
#async def auto_accept(event):
    #""" Will approve automatically if you texted them first. """
    #if event.is_private:
        #chat = await event.get_chat()
        #if not is_mongo_alive() or not is_redis_alive():
            #return
        #if isinstance(chat, User):
            #if await approval(event.chat_id) or chat.bot:
                #return
            #async for message in event.client.iter_messages(chat.id,
                                                            #reverse=True,
                                                            #limit=1):
                #if message.from_id == (await event.client.get_me()).id:
                    #await approve(chat.id)
                    #if BOTLOG:
                        #await event.client.send_message(
                            #BOTLOG_CHATID,
                            #"#AUTO-APPROVED\n" + "User: " +
                            #f"[{chat.first_name}](tg://user?id={chat.id})",
                        #)


@register(outgoing=True, pattern="^.notifoff$")
@grp_exclude()
async def notifoff(noff_event):
    """ For .notifoff command, stop getting
        notifications from unapproved PMs. """
    if await notif_off() is False:
       x = await noff_event.edit('`Notifications already silenced!`')
       time.sleep(5)
       await x.delete()
    else:
       x = await noff_event.edit("`Notifications silenced!`")
       time.sleep(5)
       await x.delete()


@register(outgoing=True, pattern="^.notifon$")
@grp_exclude()
async def notifon(non_event):
    """ For .notifoff command, get notifications from unapproved PMs. """
    if await notif_on() is False:
       x = await non_event.edit("`Notifications ain't muted!")
       time.sleep(5)
       await x.delete()
    else:
       x = await non_event.edit("`Notifications unmuted!`")
       time.sleep(5)
       await x.delete()


@register(outgoing=True, pattern="^.approve$|.a$")
@grp_exclude()
async def approvepm(apprvpm):
    """ For .approve command, give someone the permissions to PM you. """
    if apprvpm.is_private:
        chat = await apprvpm.get_chat()
        if not is_mongo_alive() or not is_redis_alive():
            await apprvpm.edit("`Database connections failing!`")
            return

        if await approve(apprvpm.chat_id) is False:
           x = await apprvpm.edit("`User was already approved!`")
           time.sleep(5)
           await x.delete()
        else:
            if apprvpm.reply_to_msg_id:
                reply = await apprvpm.get_reply_message()
                replied_user = await apprvpm.client(
                    GetFullUserRequest(reply.from_id))
                aname = replied_user.user.id
                name0 = str(replied_user.user.first_name)
                uid = replied_user.user.id

            else:
                aname = await apprvpm.client.get_entity(apprvpm.chat_id)
                name0 = str(aname.first_name)
                uid = apprvpm.chat_id
       
            await approve(chat.id)
            x = await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `approved to PM!`")
            time.sleep(5)
            await x.delete()
            
            d = (f"You have {range(1, 999)} warns left.")
            async for reply in apprvpm.client.iter_messages(
                                apprvpm.chat_id,
                                from_user='me',
                                search=d):
                            await reply.delete()

            if BOTLOG:
                await apprvpm.client.send_message(
                    BOTLOG_CHATID,
                    "#APPROVED\n" + "User: " + f"[{name0}](tg://user?id={uid})",
                )
            
            
@register(outgoing=True, pattern="^.disapprove$|.da$")
@grp_exclude()
async def disapprovepm(dapprvpm):
    """ For .disapprove command, revokes the permissions from someone to PM you. """
    if dapprvpm.is_private:
        chat = await dapprvpm.get_chat()
        if not is_mongo_alive() or not is_redis_alive():
            await dapprvpm.edit("`Database connections failing!`")
            return

        if await disapprove(dapprvpm.chat_id) is False:
           x = await dapprvpm.edit("`User isn't approved yet!`")
           time.sleep(5)
           await x.delete()
        else:
            if dapprvpm.reply_to_msg_id:
                reply = await dapprvpm.get_reply_message()
                replied_user = await dapprvpm.client(
                    GetFullUserRequest(reply.from_id))
                aname = replied_user.user.id
                name0 = str(replied_user.user.first_name)
                uid = replied_user.user.id

            else:
                aname = await dapprvpm.client.get_entity(dapprvpm.chat_id)
                name0 = str(aname.first_name)
                uid = dapprvpm.chat_id
       
            await disapprove(chat.id)
            x = await dapprvpm.edit(f"[{name0}](tg://user?id={uid}) `disapproved to PM!`")
            time.sleep(5)
            await x.delete()

            if BOTLOG:
               await dapprvpm.client.send_message(
                    BOTLOG_CHATID,
                    "#DISAPPROVED\n" + "User: " + f"[{name0}](tg://user?id={uid})",
                )


@register(outgoing=True, pattern="^.block$")
@grp_exclude()
async def blockpm(block):
    """ For .block command, block people from PMing you! """
    if not is_mongo_alive() or not is_redis_alive():
        await block.edit("`Database connections failing!`")
        return

    if await block_pm(block.chat_id) is False:
        return await block.edit("`First approve before blocking`")
        time.sleep(5)
        block_event.delete()
    else:
        await block.edit("`You are gonna be blocked from PM-ing my Master!`")

        if block.reply_to_msg_id:
            reply = await block.get_reply_message()
            replied_user = await block.client(GetFullUserRequest(reply.from_id)
                                              )
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            await block.client(BlockRequest(replied_user.user.id))
            uid = replied_user.user.id
        else:
            await block.client(BlockRequest(block.chat_id))
            aname = await block.client.get_entity(block.chat_id)
            name0 = str(aname.first_name)
            uid = block.chat_id

        await block.edit("`Blocked.`")

        if BOTLOG:
            await block.client.send_message(
                BOTLOG_CHATID,
                "#BLOCKED\n" + "User: " + f"[{name0}](tg://user?id={uid})",
            )


@register(outgoing=True, pattern="^.unblock$")
@grp_exclude()
async def unblockpm(unblock):
    """ For .unblock command, let people PMing you again! """
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client(GetFullUserRequest(reply.from_id))
        name0 = str(replied_user.user.first_name)
        if await approve(reply.from_id) is False:
            return await unblock.edit("`You haven't blocked this user yet!`")
            time.sleep(5)
            unblock_event.delete()
        else:
            return await unblock.edit("`My Master has forgiven you to PM now`")
            time.sleep(10)
            unblock_event.delete()

        await unblock.client(UnblockRequest(replied_user.user.id))

    if BOTLOG:
        await unblock.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={replied_user.user.id})"
            " was unblocc'd!.",
        )


CMD_HELP.update({
    "pmpermit": [
        "PMPermit",
        " - `.approve` or `.a`: Approve the mentioned/replied person to PM.\n"
        " - `.disapprove` or `.da`: Disapprove the mentioned/replied person to PM.\n"
        " - `.block`: Blocks the person from PMing you.\n"
        " - `.unblock`: Unblocks the person, so they can PM you again.\n"
        " - `.notifoff`: Stop any notifications coming from unapproved PMs.\n"
        " - `.notifon`: Allow notifications coming from unapproved PMs.\n"
    ]
})

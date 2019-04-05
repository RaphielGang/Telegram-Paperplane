# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for keeping control who PM you. """

from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest

from userbot import (COUNT_PM, HELPER, LOGGER, LOGGER_GROUP, NOTIF_OFF,
                     PM_AUTO_BAN, BRAIN_CHECKER)
from userbot.events import register

# ========================= CONSTANTS ============================
UNAPPROVED_MSG = ("`Bleep blop! This is a bot. Don't fret.\n\n`"
                  "`My master hasn't approved you to PM.`"
                  " `Please wait for my master to look in, he mostly approves PMs.`\n\n"
                  "`As far as I know, he doesn't usually approve retards though.`")
# =================================================================


@register(incoming=True)
async def permitpm(event):
    """ Permits people from PMing you without approval. \
        Will block retarded nibbas automatically. """
    if PM_AUTO_BAN:
        if event.sender_id in BRAIN_CHECKER:
            return
        global COUNT_PM
        if event.is_private and not (await event.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
            except AttributeError:
                return
            apprv = is_approved(event.chat_id)

            if not apprv and event.text != UNAPPROVED_MSG:
                await event.reply(UNAPPROVED_MSG)

                if NOTIF_OFF:
                    await event.client.send_read_acknowledge(event.chat_id)
                if event.chat_id not in COUNT_PM:
                    COUNT_PM.update({event.chat_id: 1})
                else:
                    COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1
                if COUNT_PM[event.chat_id] > 4:
                    await event.respond(
                        "`You were spamming my master's PM, which I don't like.`"
                        " `I'mma Report Spam.`"
                    )
                    del COUNT_PM[event.chat_id]
                    await event.client(BlockRequest(event.chat_id))
                    await event.client(ReportSpamRequest(peer=event.chat_id))
                    if LOGGER:
                        name = await event.client.get_entity(event.chat_id)
                        name0 = str(name.first_name)
                        await event.client.send_message(
                            LOGGER_GROUP,
                            "["
                            + name0
                            + "](tg://user?id="
                            + str(event.chat_id)
                            + ")"
                            + " was just another retarded nibba",
                        )


@register(outgoing=True, pattern="^.notifoff$")
async def notifoff(noff_event):
    """ For .notifoff command, stop getting notifications from unapproved PMs. """
    global NOTIF_OFF
    NOTIF_OFF = True
    await noff_event.edit("`Notifications silenced!`")


@register(outgoing=True, pattern="^.notifon$")
async def notifon(non_event):
    """ For .notifoff command, get notifications from unapproved PMs. """
    global NOTIF_OFF
    NOTIF_OFF = False
    await non_event.edit("`Notifications unmuted!`")


@register(outgoing=True, pattern="^.approve$")
async def approvepm(apprvpm):
    """ For .approve command, give someone the permissions to PM you. """
    if not apprvpm.text[0].isalpha() and apprvpm.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import approve
        except AttributeError:
            await apprvpm.edit("`Running on Non-SQL mode!`")
            return

        if apprvpm.reply_to_msg_id:
            reply = await apprvpm.get_reply_message()
            replied_user = await apprvpm.client(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            approve(replied_user.user.id)
        else:
            approve(apprvpm.chat_id)
            aname = await apprvpm.client.get_entity(apprvpm.chat_id)
            name0 = str(aname.first_name)

        await apprvpm.edit(
            f"[{name0}](tg://user?id={apprvpm.chat_id}) `Approved to PM!`"
            )

        if LOGGER:
            await apprvpm.client.send_message(
                LOGGER_GROUP,
                "#APPROVE\n"
                + "User: " + f"[{name0}](tg://user?id={apprvpm.chat_id})",
            )


@register(outgoing=True, pattern="^.block$")
async def blockpm(block):
    """ For .block command, block people from PMing you! """
    if not block.text[0].isalpha() and block.text[0] not in ("/", "#", "@", "!"):

        await block.edit("`You are gonna be blocked from PM-ing my Master!`")

        if block.reply_to_msg_id:
            reply = await block.get_reply_message()
            replied_user = await block.client(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            await block.client(BlockRequest(replied_user.user.id))
            try:
                from userbot.modules.sql_helper.pm_permit_sql import dissprove
                dissprove(replied_user.user.id)
            except Exception:
                pass
        else:
            await block.client(BlockRequest(block.chat_id))
            aname = await block.client.get_entity(block.chat_id)
            name0 = str(aname.first_name)
            try:
                from userbot.modules.sql_helper.pm_permit_sql import dissprove
                dissprove(block.chat_id)
            except Exception:
                pass

        if LOGGER:
            await block.client.send_message(
                LOGGER_GROUP,
                "#BLOCK\n"
                + "User: " + f"[{name0}](tg://user?id={block.chat_id})",
            )


@register(outgoing=True, pattern="^.unblock$")
async def unblockpm(unblock):
    """ For .unblock command, let people PMing you again! """
    if not unblock.text[0].isalpha() and unblock.text[0] \
            not in ("/", "#", "@", "!") and unblock.reply_to_msg_id:

        await unblock.edit("`My Master has forgiven you to PM now`")

        if unblock.reply_to_msg_id:
            reply = await unblock.get_reply_message()
            replied_user = await unblock.client(GetFullUserRequest(reply.from_id))
            name0 = str(replied_user.user.first_name)
            await unblock.client(UnblockRequest(replied_user.user.id))

        if LOGGER:
            await unblock.client.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={unblock.chat_id})"
                " was unblocc'd!.",
            )

HELPER.update({
    "pmpermit": "\
.approve\
\nUsage: Approves the mentioned/replied person to PM.\
\n\n.block\
\nUsage: Blocks the person from PMing you.\
\n\n.unblock\
\nUsage: Unblocks the person so they can PM you.\
\n\n.notifoff\
\nUsage: Clears any notifications of unapproved PMs.\
\n\n.notifon\
\nUsage: Allows notifications for unapproved PMs.\
"
})

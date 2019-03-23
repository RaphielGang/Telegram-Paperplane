# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest

from userbot import (COUNT_PM, HELPER, LOGGER, LOGGER_GROUP, NOTIF_OFF,
                     PM_AUTO_BAN, BRAIN_CHECKER)
from userbot.events import register

# ========================= CONSTANTS ============================
UNAPPROVED_MSG = ("`Bleep Blop! This is a Bot. Don't fret. \n\n`"
                  "`My Master hasn't approved you to PM.`"
                  "`Please wait for my Master to look in, he would mostly approve PMs.`\n\n"
                  "`As far as i know, he doesn't usually approve Retards.`")
# =================================================================


@register(incoming=True)
async def permitpm(e):
    if PM_AUTO_BAN:
        if e.sender_id in BRAIN_CHECKER:
            return
        global COUNT_PM
        if e.is_private and not (await e.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
            except:
                return
            apprv = is_approved(e.chat_id)

            if not apprv and e.text != UNAPPROVED_MSG:
                await e.reply(UNAPPROVED_MSG)

                if NOTIF_OFF:
                    await e.client.send_read_acknowledge(e.chat_id)
                if e.chat_id not in COUNT_PM:
                    COUNT_PM.update({e.chat_id: 1})
                else:
                    COUNT_PM[e.chat_id] = COUNT_PM[e.chat_id] + 1
                if COUNT_PM[e.chat_id] > 4:
                    await e.respond(
                        "`You were spamming my Master's PM, which I don't like.`"
                        "`I'mma Report Spam.`"
                    )
                    del COUNT_PM[e.chat_id]
                    await e.client(BlockRequest(e.chat_id))
                    await e.client(ReportSpamRequest(peer=e.chat_id))
                    if LOGGER:
                        name = await e.client.get_entity(e.chat_id)
                        name0 = str(name.first_name)
                        await e.client.send_message(
                            LOGGER_GROUP,
                            "["
                            + name0
                            + "](tg://user?id="
                            + str(e.chat_id)
                            + ")"
                            + " was just another retarded nibba",
                        )


@register(outgoing=True, pattern="^.notifoff$")
async def notifoff(e):
    global NOTIF_OFF
    NOTIF_OFF = True
    await e.edit("`Notifications silenced!`")


@register(outgoing=True, pattern="^.notifon$")
async def notifon(e):
    global NOTIF_OFF
    NOTIF_OFF = False
    await e.edit("`Notifications unmuted!`")


@register(outgoing=True, pattern="^.approve$")
async def approvepm(apprvpm):
    if not apprvpm.text[0].isalpha() and apprvpm.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import approve
        except:
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
    if not block.text[0].isalpha() and block.text[0] not in ("/", "#", "@", "!"):

        await block.edit("`You are gonna be blocked from PM-ing my Master!`")

        if (await block.get_reply_message()).sender_id in BRAIN_CHECKER:
            await block.edit(
                "`Block Error! Logical Malfunction.`"
                )
            return

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
    ".approve": "Approve the mentioned/replied person to PM."
})
HELPER.update({
    ".block": "Block the person on the PM."
})
HELPER.update({
    ".unblock": "Unblock the person on the PM."
})
HELPER.update({
    ".notioff": "Clear any notifications for unapproved PMs"
})
HELPER.update({
    ".notifon": "Allow notifications from unapproved PMs"
})

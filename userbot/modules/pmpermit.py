import sqlite3
import time

from telethon import events
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest

from userbot import COUNT_PM, LOGGER, LOGGER_GROUP, NOTIF_OFF, PM_AUTO_BAN, bot


@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def permitpm(e):
    if PM_AUTO_BAN:
        global COUNT_PM
        if e.is_private and not (await e.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
            except:
                return
            apprv = is_approved(e.chat_id)

            if not apprv and e.text != \
                ("`Bleep Blop! This is a Bot. Don't fret. \n\n`"
                 "`My Master hasn't approved you to PM.`"
                 "`Please wait for my Master to look in, he would mostly approve PMs.`\n\n"
                 "`As far as i know, he doesn't usually approve Retards.`"):

                await e.reply(
                    "`Bleep Blop! This is a Bot. Don't fret. \n\n`"
                    "`My Master hasn't approved you to PM.`"
                    "`Please wait for my Master to look in, he would mostly approve PMs.`\n\n"
                    "`As far as i know, he doesn't usually approve Retards.`"
                )

                if NOTIF_OFF:
                    await bot.send_read_acknowledge(e.chat_id)
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
                    await bot(BlockRequest(e.chat_id))
                    await bot(ReportSpamRequest(peer=e.chat_id))
                    if LOGGER:
                        name = await bot.get_entity(e.chat_id)
                        name0 = str(name.first_name)
                        await bot.send_message(
                            LOGGER_GROUP,
                            "["
                            + name0
                            + "](tg://user?id="
                            + str(e.chat_id)
                            + ")"
                            + " was just another retarded nibba",
                        )


@bot.on(events.NewMessage(outgoing=True,pattern="^.notifoff$"))
@bot.on(events.MessageEdited(outgoing=True,pattern="^.notifoff$"))
async def notifoff(e):
    global NOTIF_OFF
    NOTIF_OFF = True
    await e.edit("`Notifications silenced!`")


@bot.on(events.NewMessage(outgoing=True,pattern="^.notifon$"))
@bot.on(events.MessageEdited(outgoing=True,pattern="^.notifon$"))
async def notifon(e):
    global NOTIF_OFF
    NOTIF_OFF = False
    await e.edit("`Notifications unmuted!`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.approve$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.approve$"))
async def approvepm(apprvpm):
    if not apprvpm.text[0].isalpha() and apprvpm.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import approve
        except:
            await apprvpm.edit("`Running on Non-SQL mode!`")
            return

        if apprvpm.reply_to_msg_id:
            reply = await apprvpm.get_reply_message()
            replied_user = await bot(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            approve(replied_user.user.id)
        else:
            approve(apprvpm.chat_id)
            aname = await bot.get_entity(apprvpm.chat_id)
            name0 = str(aname.first_name)

        await apprvpm.edit(
            f"[{name0}](tg://user?id={apprvpm.chat_id}) `Approved to PM!`"
            )

        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={apprvpm.chat_id})"
                " was approved to PM you.",
            )


@bot.on(events.NewMessage(outgoing=True,pattern="^.block$"))
@bot.on(events.MessageEdited(outgoing=True,pattern="^.block$"))
async def blockpm(block):
    if not block.text[0].isalpha() and block.text[0] not in ("/", "#", "@", "!"):

        await block.edit("`You are gonna be blocked from PM-ing my Master!`")

        if block.reply_to_msg_id:
            reply = await block.get_reply_message()
            replied_user = await bot(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            await bot(BlockRequest(replied_user.user.id))
        else:
            await bot(BlockRequest(block.chat_id))
            aname = await bot.get_entity(block.chat_id)
            name0 = str(aname.first_name)

        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={block.chat_id})"
                " was blocc'd!.",
            )

@bot.on(events.NewMessage(outgoing=True,pattern="^.unblock$"))
@bot.on(events.MessageEdited(outgoing=True,pattern="^.unblock$"))
async def unblockpm(unblock):
    if not unblock.text[0].isalpha() and unblock.text[0] \
            not in ("/", "#", "@", "!") and unblock.reply_to_msg_id:

        await unblock.edit("`My Master has forgiven you to PM now`")

        if unblock.reply_to_msg_id:
            reply = await unblock.get_reply_message()
            replied_user = await bot(GetFullUserRequest(reply.from_id))
            name0 = str(replied_user.user.first_name)
            await bot(UnblockRequest(replied_user.user.id))

        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={unblock.chat_id})"
                " was unblocc'd!.",
            )

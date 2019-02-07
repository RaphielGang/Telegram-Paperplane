import sqlite3
import time

from telethon import events
from telethon.errors import (ChannelInvalidError, ChatAdminRequiredError,
                             UserAdminInvalidError)
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

from userbot import (BRAIN_CHECKER, LOGGER, LOGGER_GROUP, SPAM, SPAM_ALLOWANCE,
                     bot)


@bot.on(events.NewMessage(outgoing=True, pattern="^.promote$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.promote$"))
async def promote(promt):
    """ For .promote command, do promote targeted person """
    if not promt.text[0].isalpha() \
            and promt.text[0] not in ("/", "#", "@", "!"):
        chats = await promt.get_chat()
        rights = chats.admin_rights
        rights3 = chats.creator
        rights2 = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True
        )

        if not await promt.get_reply_message():
            await promt.edit("`Give a reply message`")
        elif not rights and rights3:
            rights = rights2
        elif not rights and not rights3:
            rights = None
        await promt.edit("`Trying a promote.....`")
        time.sleep(3)

        try:
            await bot(
                EditAdminRequest(promt.chat_id,
                                 (await promt.get_reply_message()).sender_id,
                                 rights)
            )

        except Exception:
            await promt.edit(
                "`You Don't have sufficient permissions to parmod`"
                )
            return
        await promt.edit("`Promoted Successfully!`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.demote$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.demote$"))
async def demote(dmod):
    """ For .demote command, do demote targeted person """
    if not dmod.text[0].isalpha() and dmod.text[0] not in ("/", "#", "@", "!"):
        rights = ChatAdminRights(
            add_admins=False,
            invite_users=False,
            change_info=False,
            ban_users=False,
            delete_messages=False,
            pin_messages=False
        )

        chat = await dmod.get_chat()
        rights = chat.admin_rights
        rights2 = chat.creator
        if not await dmod.get_reply_message():
            await dmod.edit("`Give a reply message`")
            return
        if not rights and not rights2:
            await dmod.edit("`You aren't an admin!`")
            return
        await dmod.edit("`Trying a demote.....`")
        time.sleep(3)

        try:
            await bot(
                EditAdminRequest(dmod.chat_id,
                                 (await dmod.get_reply_message())
                                 .sender_id, rights)
            )

        except Exception:
            await dmod.edit("`You Don't have sufficient permissions to demhott`")
            return
        await dmod.edit("`Demoted Successfully!`")


@bot.on(events.NewMessage(outgoing=True, pattern="^.ban$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.ban$"))
async def thanos(bon):
    """ For .ban command, do "thanos" at targeted person """
    if not bon.text[0].isalpha() and bon.text[0] not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            embed_links=True,
        )

        if (await bon.get_reply_message()).sender_id in BRAIN_CHECKER:
            await bon.edit("`Ban Error! I am not supposed to ban this user`")
            return
        await bon.edit("`Whacking the pest!`")
        time.sleep(5)
        try:
            await bot(
                EditBannedRequest(
                    bon.chat_id, (await bon.get_reply_message()).sender_id,
                    rights
                )
            )

        except Exception:
            if bon.sender_id in BRAIN_CHECKER:
                await bon.respond(
                    "<triggerban> " +
                    str((await bon.get_reply_message()).sender_id)
                )
                return

        await bon.delete()
        await bon.respond("`Banned!`")
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                str((await bon.get_reply_message()).sender_id) + " was banned.",
            )


@bot.on(events.NewMessage(outgoing=True, pattern="^.mute$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.mute$"))
async def spider(spdr):
    if not spdr.text[0].isalpha() and spdr.text[0] not in ("/", "#", "@", "!"):
        if (await spdr.get_reply_message()).sender_id in BRAIN_CHECKER:
            await spdr.edit("`Mute Error! I am not supposed to mute this user`")
            return
        try:
            from userbot.modules.sql_helper.spam_mute_sql import mute
        except Exception:
            await spdr.edit("`Running on Non-SQL mode!`")
            return

        chat = await spdr.get_chat()
        rights = chat.admin_rights
        rights2 = chat.creator
        if not rights and not rights2:
            await spdr.edit("`You aren't an admin!`")
            return
        mute(spdr.chat_id, str((await spdr.get_reply_message()).sender_id))
        await spdr.edit("`Gets a tape!`")
        time.sleep(5)

        await spdr.delete()
        await spdr.respond("`Safely taped!`")
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                str((await spdr.get_reply_message()).sender_id) +
                " was muted.",
            )


@bot.on(events.NewMessage(incoming=True, pattern="<triggerban>"))
async def triggered_ban(triggerbon):
    ban_id = int(e.text[13:])
    if triggerbon.sender_id in BRAIN_CHECKER:  # non-working module#
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            embed_links=True,
        )

    if ban_id in BRAIN_CHECKER:
        await triggerbon.edit("`Sorry Master!`")
        return

        time.sleep(5)
        await bot(EditBannedRequest(e.chat_id, ban_id, rights))
        await triggerbon.delete()
        await bot.send_message(e.chat_id,
                               "Job was done, Master! Gimme Cookies!")


@bot.on(events.NewMessage(outgoing=True, pattern="^.unmute$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.unmute$"))
async def unmute(unmot):
    if not unmot.text[0].isalpha() and unmot.text[0] not in ("/", "#", "@", "!"):
        from userbot.modules.sql_helper.spam_mute_sql import unmute

        unmute(unmot.chat_id, str((await unmot.get_reply_message()).sender_id))
        await unmot.edit("```Unmuted Successfully```")


@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def muter(moot):
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    mootd = is_muted(moot.chat_id)
    gmootd = is_gmuted(moot.sender_id)
    if mootd:
        for i in mootd:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
    for i in gmootd:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.ungmute$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.ungmute$"))
async def ungmute(ungmoot):
    if not ungmoot.text[0].isalpha() and ungmoot.text[0] \
            not in ("/", "#", "@", "!"):

        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except:
            await ungmoot.edit('`Running on Non-SQL Mode!`')
        ungmute(str((await ungmoot.get_reply_message()).sender_id))
        await ungmoot.edit("```Ungmuted Successfully```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.gmute$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.gmute$"))
async def gspider(gspdr):
    if not gspdr.text[0].isalpha() and gspdr.text[0] not in ("/", "#", "@", "!"):
        if (await gspdr.get_reply_message()).sender_id in BRAIN_CHECKER:
            await gspdr.edit("`Mute Error! Couldn't mute this user`")
            return
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except Exception as err:
            print(err)
            await gspdr.edit("`Running on Non-SQL mode!`")
            return

        gmute(str((await e.get_reply_message()).sender_id))
        await gspdr.edit("`Grabs a huge, sticky duct tape!`")
        time.sleep(5)
        await gspdr.delete()
        await gspdr.respond("`Taped!`")

        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                str((await gspdr.get_reply_message()).sender_id)
                + " was muted.",
            )

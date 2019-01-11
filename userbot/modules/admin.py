from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from telethon.errors import UserAdminInvalidError
from telethon.errors import ChatAdminRequiredError
from telethon.errors import ChannelInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChannelAdminRights
import time
import sqlite3
from telethon import TelegramClient, events
from userbot import bot, SPAM, SPAM_ALLOWANCE, BRAIN_CHECKER, LOGGER_GROUP, LOGGER


@bot.on(events.NewMessage(outgoing=True, pattern="^.wizard$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.wizard$"))
async def wizzard(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        rights = ChannelAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
            invite_link=True,
        )
        await e.edit("`Wizard waves his wand!`")
        time.sleep(3)
        await bot(
            EditAdminRequest(e.chat_id, (await e.get_reply_message()).sender_id, rights)
        )
        await e.edit("A perfect magic has happened!")


@bot.on(events.NewMessage(outgoing=True, pattern="^.thanos$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.thanos$"))
async def thanos(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        rights = ChannelBannedRights(
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
        if (await e.get_reply_message()).sender_id in BRAIN_CHECKER:
            await e.edit("`Ban Error! Couldn't ban this user`")
            return
        await e.edit("`Thanos snaps!`")
        time.sleep(5)
        try:
            await bot(
                EditBannedRequest(
                    e.chat_id, (await e.get_reply_message()).sender_id, rights
                )
            )
        except:
            if e.sender_id in BRAIN_CHECKER:
                await e.respond(
                    "<triggerban> " + str((await e.get_reply_message()).sender_id)
                )
                return
        await e.delete()
        await bot.send_file(
            e.chat_id, "https://media.giphy.com/media/xUOxfgwY8Tvj1DY5y0/source.gif"
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                str((await e.get_reply_message()).sender_id) + " was banned.",
            )


@bot.on(events.NewMessage(outgoing=True, pattern="^.spider$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.spider$"))
async def spider(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if (await e.get_reply_message()).sender_id in BRAIN_CHECKER:
            await e.edit("`Mute Error! Couldn't mute this user`")
            return
        try:
            from userbot.modules.sql_helper.spam_mute_sql import mute
        except Exception as er:
            await e.edit("`Running on Non-SQL mode!`")
            return
        mute(e.chat_id, str((await e.get_reply_message()).sender_id))
        await e.edit("`Spiderman nabs him!`")
        time.sleep(5)
        await e.delete()
        await bot.send_file(
            e.chat_id, "https://image.ibb.co/mNtVa9/ezgif_2_49b4f89285.gif"
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                str((await e.get_reply_message()).sender_id) + " was muted.",
            )


@bot.on(events.NewMessage(incoming=True, pattern="<triggerban>"))
async def triggered_ban(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        ban_id = int(e.text[13:])
        if e.sender_id in BRAIN_CHECKER:  # non-working module#
            rights = ChannelBannedRights(
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
                await e.edit("`Sorry Master!`")
                return
            await e.edit("`Command from my Master!`")
            time.sleep(5)
            await bot(EditBannedRequest(e.chat_id, ban_id, rights))
            await e.delete()
            await bot.send_message(e.chat_id, "Job was done, Master! Gimme Cookies!")


@bot.on(events.NewMessage(incoming=True, pattern="<triggermute>"))
async def triggered_mute(e):
    message = e.text
    ban_id = int(e.text[14:])
    if e.sender_id in BRAIN_CHECKER:
        rights = ChannelBannedRights(
            until_date=None,
            view_messages=True,
            send_messages=True,
            send_media=True,
            send_stickers=True,  # non-working module#
            send_gifs=True,
            send_games=True,
            send_inline=True,
            embed_links=True,
        )
        if ban_id in BRAIN_CHECKER:
            await e.edit("`Sorry Master!`")
            return
        await e.edit("`Command from my Master!`")
        time.sleep(5)
        await bot(
            EditBannedRequest(
                e.chat_id, (await e.get_reply_message()).sender_id, rights
            )
        )
        await e.delete()
        await bot.send_file(e.chat_id, "Job was done, Master! Gimme Cookies!")


@bot.on(events.NewMessage(outgoing=True, pattern="^.speak$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.speak$"))
async def unmute(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        from userbot.modules.sql_helper.spam_mute_sql import unmute

        unmute(e.chat_id, str((await e.get_reply_message()).sender_id))
        await e.edit("```Unmuted Successfully```")


@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def muter(e):
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    L = is_muted(e.chat_id)
    K = is_gmuted(e.sender_id)
    if L:
        for i in L:
            if str(i.sender) == str(e.sender_id):
                await e.delete()
    for i in K:
        if i.sender == str(e.sender_id):
            await e.delete()

@bot.on(events.NewMessage(outgoing=True, pattern="^.ungmute$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.ungmute$"))
async def unmute(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except:
            await e.edit('`Running on Non-SQL Mode!`')
        ungmute(str((await e.get_reply_message()).sender_id))
        await e.edit("```Ungmuted Successfully```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.gspider$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.gspider$"))
async def spider(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if (await e.get_reply_message()).sender_id in BRAIN_CHECKER:
            await e.edit("`Mute Error! Couldn't mute this user`")
            return
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except Exception as er:
            print(er)
            await e.edit("`Running on Non-SQL mode!`")
            return
        gmute(str((await e.get_reply_message()).sender_id))
        await e.edit("`Spiderman nabs him!`")
        time.sleep(5)
        await e.delete()
        await bot.send_file(
            e.chat_id, "https://image.ibb.co/mNtVa9/ezgif_2_49b4f89285.gif"
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                str((await e.get_reply_message()).sender_id) + " was muted.",
            )

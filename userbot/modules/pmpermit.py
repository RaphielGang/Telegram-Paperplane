# Special module to block pms automatically
from telethon.tl.functions.contacts import BlockRequest
import sqlite3
from telethon import TelegramClient, events
from userbot import bot
from userbot import PM_AUTO_BAN
from userbot import COUNT_PM
from userbot import LOGGER, LOGGER_GROUP


@bot.on(events.NewMessage(incoming=True))
async def permitpm(e):
    if PM_AUTO_BAN:
        global COUNT_PM
        if e.is_private and not (await e.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
            except:
                return
            E = is_approved(e.chat_id)
            if not E:
                await e.reply(
                    "`Bleep Blop! This is a Bot. Don't fret. \n\nMy Master hasn't approved you to PM. \
Please wait for my Master to look in, he would mostly approve PMs.\n\n\
As far as i know, he doesn't usually approve Retards.`"
                )
                if e.chat_id not in COUNT_PM:
                    COUNT_PM.update({e.chat_id: 1})
                else:
                    COUNT_PM[e.chat_id] = COUNT_PM[e.chat_id] + 1
                if COUNT_PM[e.chat_id] > 4:
                    await e.respond(
                        "`You were spamming my Master's PM, which I don't like. I'mma Report Spam.`"
                    )
                    del COUNT_PM[e.chat_id]
                    await bot(BlockRequest(e.chat_id))
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


@bot.on(events.NewMessage(outgoing=True, pattern="^.approvepm$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.approvepm$"))
async def approvepm(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import approve
        except:
            await e.edit("`Running on Non-SQL mode!`")
            return
        approve(e.chat_id)
        await e.edit("`Approved to PM!`")
        if LOGGER:
            aname = await bot.get_entity(e.chat_id)
            name0 = str(aname.first_name)
            await bot.send_message(
                LOGGER_GROUP,
                "["
                + name0
                + "](tg://user?id="
                + str(e.chat_id)
                + ")"
                + " was approved to PM you.",
            )

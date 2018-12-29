from async_generator import aclosing
import asyncio
from telethon import TelegramClient, events
from userbot import bot
from userbot import LOGGER, LOGGER_GROUP
import time


@bot.on(events.NewMessage(outgoing=True, pattern="^.fastpurge$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.fastpurge$"))
async def fastpurger(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        chat = await e.get_input_chat()
        msgs = []
        count = 0
        async with aclosing(bot.iter_messages(chat, min_id=e.reply_to_msg_id)) as h:
            async for m in h:
                msgs.append(m)
                count = count + 1
                msgs.append(e.reply_to_msg_id)
                if len(msgs) == 100:
                    await bot.delete_messages(chat, msgs)
                    msgs = []
        if msgs:
            await bot.delete_messages(chat, msgs)
        r = await bot.send_message(
            e.chat_id,
            "`Fast purge complete!\n`Purged "
            + str(count)
            + " messages. **This auto-generated message shall be self destructed in 2 seconds.**",
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "Purge of " + str(count) + " messages done successfully."
            )
        time.sleep(2)
        i = 1
        await r.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.purgeme"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.purgeme"))
async def purgeme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        count = int(message[9:])
        i = 1
        async for message in bot.iter_messages(e.chat_id, from_user="me"):
            if i > count + 1:
                break
            i = i + 1
            await message.delete()
        r = await bot.send_message(
            e.chat_id,
            "`Purge complete!` Purged "
            + str(count)
            + " messages. **This auto-generated message shall be self destructed in 2 seconds.**",
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "Purge of " + str(count) + " messages done successfully."
            )
        time.sleep(2)
        i = 1
        await r.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.delmsg$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.delmsg$"))
async def delmsg(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        i = 1
        async for message in bot.iter_messages(e.chat_id, from_user="me"):
            if i > 2:
                break
            i = i + 1
            await message.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.editme"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.editme"))
async def editer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        string = str(message[8:])
        i = 1
        async for message in bot.iter_messages(e.chat_id, from_user="me"):
            if i == 2:
                await message.edit(string)
                await e.delete()
                break
            i = i + 1
        if LOGGER:
            await bot.send_message(LOGGER_GROUP, "Edit query was executed successfully")


@bot.on(events.NewMessage(outgoing=True, pattern="^.sd"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sd"))
async def selfdestruct(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[4:6])
        text = str(e.text[6:])
        text = (
            text
            + "`This message shall be self-destructed in "
            + str(counter)
            + " seconds`"
        )
        await e.delete()
        x=await bot.send_message(e.chat_id, text)
        time.sleep(counter)
        await x.delete()
        if LOGGER:
            await bot.send_message(LOGGER_GROUP, "sd query done successfully")

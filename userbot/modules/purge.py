import asyncio
import time

from async_generator import aclosing
from telethon import events
from telethon.errors import rpcbaseerrors

from userbot import LOGGER, LOGGER_GROUP, bot


@bot.on(events.NewMessage(outgoing=True, pattern="^.purge$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.purge$"))
async def fastpurger(purg):
    if not purg.text[0].isalpha() and purg.text[0] not in ("/", "#", "@", "!"):
        chat = await purg.get_input_chat()
        msgs = []
        count = 0
        async with aclosing(
                bot.iter_messages(chat, min_id=purg.reply_to_msg_id)
                )as replies:

            async for smsgs in replies:
                msgs.append(smsgs)
                count = count + 1
                msgs.append(purg.reply_to_msg_id)
                if len(msgs) == 100:
                    await bot.delete_messages(chat, msgs)
                    msgs = []

        if msgs:
            await bot.delete_messages(chat, msgs)
        done = await bot.send_message(
            purg.chat_id,
            "`Fast purge complete!\n`Purged "
            + str(count)
            + " messages. **This auto-generated message shall be self destructed in 2 seconds.**",
        )

        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "Purge of " + str(count) + " messages done successfully."
            )
        time.sleep(2)
        await done.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.purgeme"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.purgeme"))
async def purgeme(delme):
    if not delme.text[0].isalpha() and delme.text[0] not in ("/", "#", "@", "!"):
        message = delme.text
        self_id = await bot.get_peer_id('me')
        count = int(message[9:])
        i = 1

        async for message in bot.iter_messages(delme.chat_id, self_id):
            if i > count + 1:
                break
            i = i + 1
            await message.delete()

        smsg = await bot.send_message(
            delme.chat_id,
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
        await smsg.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.delmsg$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.delmsg$"))
async def delmsg(delme):
    if not delme.text[0].isalpha() and delme.text[0] not in ("/", "#", "@", "!"):
        msg_src = await delme.get_reply_message()
        if delme.reply_to_msg_id:
            try:
                await msg_src.delete()
                await delme.delete()
                if LOGGER:
                    await bot.send_message(
                        LOGGER_GROUP,
                        "Deletion of message was successful"
                        )
            except Exception is rpcbaseerrors.BadRequestError:
                if LOGGER:
                    await bot.send_message(
                        LOGGER_GROUP,
                        "Well, I can't delete a message"
                        )


@bot.on(events.NewMessage(outgoing=True, pattern="^.editme"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.editme"))
async def editer(edit):
    if not edit.text[0].isalpha() and edit.text[0] not in ("/", "#", "@", "!"):
        message = edit.text
        chat = await edit.get_input_chat()
        self_id = await bot.get_peer_id('me')
        string = str(message[8:])
        i = 1
        async for message in bot.iter_messages(chat, self_id):
            if i == 2:
                await message.edit(string)
                await edit.delete()
                break
            i = i + 1
        if LOGGER:
            await bot.send_message(LOGGER_GROUP, "Edit query was executed successfully")


@bot.on(events.NewMessage(outgoing=True, pattern="^.sd"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sd"))
async def selfdestruct(destroy):
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[4:6])
        text = str(destroy.text[6:])
        text = (
            text
            + "`This message shall be self-destructed in "
            + str(counter)
            + " seconds`"
        )
        await destroy.delete()
        smsg = await bot.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()
        if LOGGER:
            await bot.send_message(LOGGER_GROUP, "sd query done successfully")

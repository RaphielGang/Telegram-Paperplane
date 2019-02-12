from asyncio import wait

from telethon import events

from userbot import bot


@bot.on(events.NewMessage(outgoing=True, pattern="^.spam"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.spam"))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])

        await wait(
            [e.respond(spam_message) for i in range(counter)]
            )

        await e.delete()
        await bot.send_message(LOGGER_GROUP, "Spammed successfully")


@bot.on(events.NewMessage(outgoing=True, pattern="^.bigspam"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.bigspam"))
async def bigspam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[9:13])
        spam_message = str(e.text[13:])

        for i in range(1, counter):
            await e.respond(spam_message)

        await e.delete()
        await bot.send_message(LOGGER_GROUP, "bigspam was successful")


@bot.on(events.NewMessage(outgoing=True, pattern="^.picspam"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.picspam"))
async def tiny_pic_spam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        text = message.split()
        counter = int(text[1])
        link = str(text[2])
        for i in range(1, counter):
            await bot.send_file(e.chat_id, link)
        await e.delete()
        await bot.send_message(LOGGER_GROUP, "PicSpam was successful")

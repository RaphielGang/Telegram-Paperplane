import os
import re
import subprocess
import time
from datetime import datetime, timedelta

import urbandict
import wikipedia
from google_images_download import google_images_download
from googletrans import Translator
from gtts import gTTS
from telethon import TelegramClient, events

from userbot import LOGGER, LOGGER_GROUP, bot

langi = "en"


@bot.on(events.NewMessage(outgoing=True, pattern="^.img (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.img (.*)"))
async def img_sampler(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Processing...")
        start = round(time.time() * 1000)
        s = e.pattern_match.group(1)
        lim = re.findall(r"lim=\d+", s)
        try:
            lim = lim[0]
            lim = lim.replace("lim=", "")
            s = s.replace("lim=" + lim[0], "")
        except IndexError:
            lim = 2
        response = google_images_download.googleimagesdownload()
        arguments = {
            "keywords": s,
            "limit": lim,
            "format": "jpg",
        }  # creating list of arguments
        paths = response.download(arguments)  # passing the arguments to the function
        lst = paths[s]
        await bot.send_file(await bot.get_input_entity(e.chat_id), lst)
        end = round(time.time() * 1000)
        msstartend = int(end) - int(start)
        await e.delete()


@bot.on(events.NewMessage(outgoing=True, pattern=r"^.google (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern=r"^.google (.*)"))
async def gsearch(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        match = e.pattern_match.group(1)
        result_ = subprocess.run(["gsearch", match], stdout=subprocess.PIPE)
        result = str(result_.stdout.decode())
        await e.edit(
            "**Search Query:**\n`" + match + "`\n\n**Result:**\n" + result
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                "Google Search query " + match + " was executed successfully",
            )


@bot.on(events.NewMessage(outgoing=True, pattern=r"^.wiki (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern=r"^.wiki (.*)"))
async def wiki(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        match = e.pattern_match.group(1)
        result = wikipedia.summary(match)
        await e.edit(
            "**Search:**\n`" + match + "`\n\n**Result:**\n" + result
        )
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "Wiki query " + match + " was executed successfully"
            )


@bot.on(events.NewMessage(outgoing=True, pattern="^.ud (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.ud (.*)"))
async def ud(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Processing...")
        str = e.pattern_match.group(1)
        mean = urbandict.define(str)
        if len(mean) >= 0:
            await e.edit(
                "Text: **"
                + str
                + "**\n\nMeaning: **"
                + mean[0]["def"]
                + "**\n\n"
                + "Example: \n__"
                + mean[0]["example"]
                + "__"
            )
            if LOGGER:
                await bot.send_message(
                    LOGGER_GROUP, "ud query " + str + " executed successfully."
                )
        else:
            await e.edit("No result found for **" + str + "**")


@bot.on(events.NewMessage(outgoing=True, pattern="^.tts"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.tts"))
async def tts(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        replye = e.text
        if replye[5:]:
            message = str(replye[5:])
        elif textx:
            message = textx
            message = str(message.message)
        current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
        tts = gTTS(message, langi)
        tts.save("k.mp3")
        with open("k.mp3", "rb") as f:
            linelist = list(f)
            linecount = len(linelist)
        if linecount == 1:
            try:  # tts on personal chats is broken
                tts = gTTS(message, langi)
                tts.save("k.mp3")
            except:
                await e.edit("`Some Internal Error! Try Again!`")
                return
        with open("k.mp3", "r") as speech:
            await bot.send_file(e.chat_id, "k.mp3", voice_note=True)
            os.remove("k.mp3")
            if LOGGER:
                await bot.send_message(
                    LOGGER_GROUP, "tts of " + message + " executed successfully!"
                )
            await e.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.trt"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.trt"))
async def translateme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global langi
        translator = Translator()
        textx = await e.get_reply_message()
        message = e.text
        if message[4:]:
            message = str(message[4:])
        elif textx:
            message = textx
            message = str(message.message)
        reply_text = translator.translate(message, dest=langi).text
        reply_text = "**Source:** `\n" + message + "`**\n\nTranslation: **`\n" + reply_text  + "`"
        await bot.send_message(e.chat_id, reply_text)
        await e.delete()
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                "Translate query " + message + " was executed successfully",
            )


@bot.on(events.NewMessage(pattern=".lang", outgoing=True))
@bot.on(events.MessageEdited(pattern=".lang", outgoing=True))
async def lang(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global langi
        message = await bot.get_messages(e.chat_id)
        langi = str(message[0].message[6:])
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "tts language changed to **" + langi + "**"
            )
            await e.edit("tts language changed to **" + langi + "**")

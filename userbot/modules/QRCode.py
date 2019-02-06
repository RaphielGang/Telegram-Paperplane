import asyncio
import os
from datetime import datetime

import requests
from telethon import TelegramClient, events

from userbot import LOGGER, LOGGER_GROUP, bot

download_directory = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")


def progress(current, total):
    print(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@bot.on(events.NewMessage(pattern=r"^.getqr$", outgoing=True))
@bot.on(events.MessageEdited(pattern=r"^.getqr$", outgoing=True))
async def parseqr(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.fwd_from:
            return
        start = datetime.now()
        downloaded_file_name = await bot.download_media(
            await e.get_reply_message(), download_directory, progress_callback=progress
        )
        url = "https://api.qrserver.com/v1/read-qr-code/?outputformat=json"
        files = {"file": open(downloaded_file_name, "rb")}
        r = requests.post(url, files=files).json()
        qr_contents = r[0]["symbol"][0]["data"]
        os.remove(downloaded_file_name)
        end = datetime.now()
        ms = (end - start).seconds
        await e.edit(
            "Obtained QRCode contents in {} seconds.\n{}".format(ms, qr_contents)
        )


@bot.on(events.NewMessage(pattern=r".makeqr ?(.*)", outgoing=True))
async def make_qr(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.fwd_from:
            return
        start = datetime.now()
        input_str = e.pattern_match.group(1)
        message = "SYNTAX: `.makeqr <long text to include>`"
        reply_msg_id = e.message.id
        if input_str:
            message = input_str
        elif e.reply_to_msg_id:
            previous_message = await e.get_reply_message()
            reply_msg_id = previous_message.id
            if previous_message.media:
                downloaded_file_name = await bot.download_media(
                    previous_message, download_directory, progress_callback=progress
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                message = ""
                for m in m_list:
                    message += m.decode("UTF-8") + "\r\n"
                os.remove(downloaded_file_name)
            else:
                message = previous_message.message
        else:
            message = "SYNTAX: `.makeqr <long text to include>`"
        url = "https://api.qrserver.com/v1/create-qr-code/?data={}&size=200x200&charset-source=UTF-8&charset-target=UTF-8&ecc=L&color=0-0-0&bgcolor=255-255-255&margin=1&qzone=0&format=jpg"
        r = requests.get(url.format(message), stream=True)
        required_file_name = download_directory + " " + str(datetime.now()) + ".webp"
        with open(required_file_name, "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        await bot.send_file(
            e.chat_id,
            required_file_name,
            reply_to=reply_msg_id,
            progress_callback=progress,
        )
        os.remove(required_file_name)
        end = datetime.now()
        ms = (end - start).seconds
        await e.edit("Created QRCode in {} seconds".format(ms))
        await asyncio.sleep(5)
        await e.delete()

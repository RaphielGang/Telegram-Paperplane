# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'makeqr and getqr' which is MPL
# License: MPL and OSSRPL
""" Userbot module containing commands related to QR Codes. """

import os
from asyncio import sleep
from datetime import datetime

from requests import post, get

from userbot import CMD_HELP
from userbot.events import register, errors_handler


def progress(current, total):
    """ Calculate and return the download progress with given arguments. """
    print("Downloaded {} of {}\nCompleted {}".format(current, total,
                                                     (current / total) * 100))


@register(pattern=r"^.getqr$", outgoing=True)
@errors_handler
async def parseqr(qr_e):
    """ For .getqr command, get QR Code content from the replied photo. """
    if not qr_e.text[0].isalpha() and qr_e.text[0] not in ("/", "#", "@", "!"):
        if qr_e.fwd_from:
            return
        start = datetime.now()
        downloaded_file_name = await qr_e.client.download_media(
            await qr_e.get_reply_message(), progress_callback=progress)
        url = "https://api.qrserver.com/v1/read-qr-code/?outputformat=json"
        file = open(downloaded_file_name, "rb")
        files = {"file": file}
        resp = post(url, files=files).json()
        qr_contents = resp[0]["symbol"][0]["data"]
        file.close()
        os.remove(downloaded_file_name)
        end = datetime.now()
        duration = (end - start).seconds
        await qr_e.edit("Obtained QRCode contents in {} seconds.\n{}".format(
            duration, qr_contents))


@register(pattern=r".makeqr(?: |$)([\s\S]*)", outgoing=True)
@errors_handler
async def make_qr(qrcode):
    """ For .makeqr command, make a QR Code containing the given content. """
    if not qrcode.text[0].isalpha() and qrcode.text[0] not in ("/", "#", "@",
                                                               "!"):
        if qrcode.fwd_from:
            return
        start = datetime.now()
        input_str = qrcode.pattern_match.group(1)
        message = "SYNTAX: `.makeqr <long text to include>`"
        reply_msg_id = None
        if input_str:
            message = input_str
        elif qrcode.reply_to_msg_id:
            previous_message = await qrcode.get_reply_message()
            reply_msg_id = previous_message.id
            if previous_message.media:
                downloaded_file_name = await qrcode.client.download_media(
                    previous_message, progress_callback=progress)
                m_list = None
                with open(downloaded_file_name, "rb") as file:
                    m_list = file.readlines()
                message = ""
                for media in m_list:
                    message += media.decode("UTF-8") + "\r\n"
                os.remove(downloaded_file_name)
            else:
                message = previous_message.message

        url = "https://api.qrserver.com/v1/create-qr-code/?data={}&\
size=200x200&charset-source=UTF-8&charset-target=UTF-8\
&ecc=L&color=0-0-0&bgcolor=255-255-255\
&margin=1&qzone=0&format=jpg"

        resp = get(url.format(message), stream=True)
        required_file_name = "temp_qr.webp"
        with open(required_file_name, "w+b") as file:
            for chunk in resp.iter_content(chunk_size=128):
                file.write(chunk)
        await qrcode.client.send_file(
            qrcode.chat_id,
            required_file_name,
            reply_to=reply_msg_id,
            progress_callback=progress,
        )
        os.remove(required_file_name)
        duration = (datetime.now() - start).seconds
        await qrcode.edit("Created QRCode in {} seconds".format(duration))
        await sleep(5)
        await qrcode.delete()


CMD_HELP.update({
    'getqr':
    ".getqr\
\nUsage: Get the QR Code content from the replied QR Code."
})

CMD_HELP.update({
    'makeqr':
    ".makeqr <content>)\
\nUsage: Make a QR Code from the given content.\
\nExample: .makeqr www.google.com"
})

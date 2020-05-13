# Copyright (C) 2019 The Raphielscape Company LLC, Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL

""" Userbot module containing commands related to QR Codes. """

import os

import pyqrcode
import qrtools
import random

from userbot import CMD_HELP
from userbot.events import register


def progress(current, total):
    """ Calculate and return the download progress with given arguments. """
    print("Downloaded {} of {}\nCompleted {}".format(current, total,
                                                     (current / total) * 100))


@register(pattern=r"^.parseqr$", outgoing=True)
async def parseqr(qr_e):
    """ Decode Qr Code """
    if qr_e.fwd_from:
        return
    qrcodet = await qr_e.client.download_media(
        await qr_e.get_reply_message(), progress_callback=progress)
    qr = qrtools.QR()
    qr.decode(qrcodet)
    os.remove(qrcodet)
    await qr_e.edit(f"Decoded QR:\n {qr.data}")


@register(pattern=r"^.makeqr(?: |$)([\s\S]*)", outgoing=True)
async def make_qr(qrstr):
    """ Make QR """
    if qrstr.fwd_from:
        return
    input_str = qrstr.pattern_match.group(1)
    message = "Invalid Input"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif qrstr.reply_to_msg_id:
        prev = await qrstr.get_reply_message()
        reply_msg_id = prev.id
        if prev.media:
            file = await qrstr.client.download_media(prev, progress_callback=progress)
            with open(file, "rb") as filed:
                m_list = filed.readlines()
            message = ""
            for media in m_list:
                message += media.decode("UTF-8") + "\r\n"
            os.remove(file)
        else:
            message = prev.message

    qr = pyqrcode.create(message)
    save_qr = random.randint(0, 100)
    qr.png(f"{save_qr}", scale=7)
    await qrstr.client.send_file(
        qrstr.chat_id,
        save_qr,
        reply_to=reply_msg_id,
        progress_callback=progress,
    )
    os.remove(save_qr)
    await qrstr.delete()


CMD_HELP.update({"qr codes": ['QR Codes',
    " - `.getqr`: Get the QR Code content from the replied QR Code.\n"
    " - `.makeqr <content>`: Make a QR Code from the given message (text, link, etc...).\n"]
})

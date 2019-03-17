# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

import io
import math
import urllib.request

from PIL import Image
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from userbot import bot, HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.kang")
async def kang(args):
    if not args.text[0].isalpha() and args.text[0] not in ("/", "#", "@", "!"):
        user = await bot.get_me()
        userid = user.id
        username = user.username
        if not username:
            username = user.first_name
        packname = f"a{userid}_by_{username}"
        response = urllib.request.urlopen(urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')
        message = await args.get_reply_message()
        photo = None
        emoji = "🌚"

        if message and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.photo
                photo = await bot.download_media(message=photo)
            elif "image" in message.media.document.mime_type.split('/'):
                photo = io.BytesIO()
                await bot.download_file(message.media.document, photo)
                if DocumentAttributeFilename(file_name='sticker.webp') in message.media.document.attributes:
                    emoji = message.media.document.attributes[1].alt
            else:
                await args.edit("INVALID MEDIA BOI")
                return
        else:
            await args.edit("Reply to photo to kang it bruh")
            return

        if photo:
            im = Image.open(photo)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512/size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512/size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)

            file = io.BytesIO()
            file.name = "sticker.png"
            im.save(file, "PNG")
            if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
                async with bot.conversation('Stickers') as conv:
                    await conv.send_message('/addsticker')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    await conv.get_response()
                    file.seek(0)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_file(file, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message('/done')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
            else:
                await args.edit("userbot sticker pack doesn't exist! Making a new one!")
                async with bot.conversation('Stickers') as conv:
                    await conv.send_message('/newpack')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(f"@{username}'s userbot pack")
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/publish")
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message(packname)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)

            await args.edit(f"sticker added! Your pack can be found [here](t.me/addstickers/{packname})", parse_mode='md')

HELPER.update({
    "kang": "Kang very important module. Please kang this. Made by @rupansh"
})

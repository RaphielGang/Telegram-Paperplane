# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for kanging stickers or making new ones. """

import io
import math
import urllib.request

from PIL import Image
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from userbot import bot, HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.kang")
async def kang(args):
    """ For .kang command, kangs stickers or creates new ones. """
    if not args.text[0].isalpha() and args.text[0] not in ("/", "#", "@", "!"):
        user = await bot.get_me()
        if not user.username:
            user.username = user.first_name
        message = await args.get_reply_message()
        photo = None
        emojibypass = False

        if message and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = io.BytesIO()
                photo = await bot.download_media(message.photo, photo)
            elif "image" in message.media.document.mime_type.split('/'):
                photo = io.BytesIO()
                await bot.download_file(message.media.document, photo)
                if (DocumentAttributeFilename(file_name='sticker.webp')
                        in message.media.document.attributes):
                    emoji = message.media.document.attributes[1].alt
                    emojibypass = True
            else:
                await args.edit("`Unsupported File!`")
                return
        else:
            await args.edit("`Reply to photo to kang it bruh`")
            return

        if photo:
            image = await resize_photo(photo)
            splat = args.text.split()
            if not emojibypass:
                emoji = "🤔"
            pack = "1"
            if len(splat) == 3:
                pack = splat[2]     #User sent both
                emoji = splat[1]
            elif len(splat) == 2:
                if splat[1].isnumeric():
                    #User wants to push into different pack, but is okay with thonk as emote.
                    pack = int(splat[1])
                else:
                    #User sent just custom emote, wants to push to default pack
                    emoji = splat[1]

            packname = f"a{user.id}_by_{user.username}_{pack}"
            response = urllib.request.urlopen(
                urllib.request.Request(f'http://t.me/addstickers/{packname}')
            )
            htmlstr = response.read().decode("utf8").split('\n')
            file = io.BytesIO()
            file.name = "sticker.png"
            image.save(file, "PNG")
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
                await args.edit("Userbot sticker pack doesn't exist! Making a new one!")
                async with bot.conversation('Stickers') as conv:
                    await conv.send_message('/newpack')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(f"@{user.username}'s userbot pack {pack}")
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
                    await conv.send_message("/skip")
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message(packname)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)

            await args.edit(
                f"Sticker added! Your pack can be found [here](t.me/addstickers/{packname})",
                parse_mode='md'
            )

async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
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
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


HELPER.update({
    "kang": ".kang\
\nUsage: Reply .kang to a sticker or an image to kang it to your userbot pack.\
\n\n.kang [emoji('s)]\
\nUsage: Works just like .kang but uses the emoji('s) you picked.\
\n\n.kang [number]\
\nUsage: Kang's the sticker/image to the specified pack but uses 🤔 as emoji.\
\n\n\nPlease kang this. Made by @rupansh."
})

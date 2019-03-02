import hashlib
import io
import math
from PIL import Image
import urllib.request

from telethon import TelegramClient, events
from telethon.tl.types import InputStickerSetID, InputStickerSetItem, MessageMediaDocument, MessageMediaPhoto

from userbot import bot


@bot.on(events.NewMessage(pattern="^.kang", outgoing=True))
@bot.on(events.MessageEdited(pattern="^.kang", outgoing=True))
async def kang(args):
    if not args.text[0].isalpha() and args.text[0] not in ("/", "#", "@", "!"):
        userid = args.sender.id
        username = args.sender.username
        hash = hashlib.sha1(bytearray(userid)).hexdigest()
        packname = f"a{hash[:20]}_by_{username}"
        response = urllib.request.urlopen(urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')
        message = await args.get_reply_message()
        photo = None

        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.photo
                photo = await bot.download_media(message=photo)
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document.mime_type in ["image/jpeg", "image/png"]:
                    photo = io.BytesIO()
                    await bot.download_file(message.media.document, photo)
            else:
                await args.edit("INVALID MEDIA BOI")
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
                    await conv.send_message(packname)
                    await conv.get_response()
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    await conv.get_response()
                    await conv.send_message("🌚")
                    await conv.get_response()
                    await conv.send_message('/done')
                    await conv.get_response()
            else:
                await args.edit("userbot sticker pack doesn't exist! Making a new one!")
                async with bot.conversation('Stickers') as conv:
                    await conv.send_message('/newpack')
                    await conv.get_response()
                    await conv.send_message(f"@{username}'s userbot pack")
                    await conv.get_response()
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    await conv.get_response()
                    await conv.send_message("🌚")
                    await conv.get_response()
                    await conv.send_message("/publish")
                    await conv.get_response()
                    await conv.send_message(packname)
                    await conv.get_response()

            await args.edit(f"sticker added! Your pack can be found [here](t.me/addstickers/{packname})", parse_mode='md')

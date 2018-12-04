from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityMentionName, MessageMediaPhoto, MessageMediaDocument
from telethon.utils import get_input_location
from telethon.errors import PhotoCropSizeSmallError, ImageProcessFailedError
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from userbot import bot
import io
import re
from telethon.tl.functions.channels import EditPhotoRequest


@bot.on(events.NewMessage(outgoing=True,pattern='^.ppic$'))
async def profile_photo(e):
    if not e.text[0].isalpha():
        message = await e.get_reply_message()
        photo = None
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.photo
                photo = await bot.download_media(message=photo)
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document.mime_type in ['image/jpeg', 'image/png']:
                    photo = message.media.document
                    photo = await bot.download_file(photo)
                    photo = io.BytesIO(photo)
                    photo.name = 'image.jpeg' # small hack for documents images
            else:
                await e.edit('```The extension of the media entity is invalid.```')

        if photo:
            file = await bot.upload_file(photo)
            try:
                await bot(UploadProfilePhotoRequest(file))
                await e.edit('```Profile Picture Changed```')

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await e.edit('```The image is too small```')
                elif isinstance(exc, ImageProcessFailedError):
                    await e.edit('```Failure while processing image```')


@bot.on(events.NewMessage(outgoing=True,pattern='^.xpic$'))
async def profile_photo(e):
    if not e.text[0].isalpha():
        message = await e.get_reply_message()
        photo = None
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.photo
                photo = await bot.download_media(message=photo)
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document.mime_type in ['image/jpeg', 'image/png']:
                    photo = message.media.document
                    photo = await bot.download_file(photo)
                    photo = io.BytesIO(photo)
                    photo.name = 'image.jpeg' # small hack for documents images
            else:
                await e.edit('```The extension of the media entity is invalid.```')

        if photo:
            file = await bot.upload_file(photo)
            try:
                await bot(EditPhotoRequest(e.chat_id,file))
                await e.edit('```Chat Picture Changed```')

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await e.edit('```The image is too small```')
                elif isinstance(exc, ImageProcessFailedError):
                    await e.edit('```Failure while processing image```')
                else:
                    await e.edit('`Some issue with updating the pic, maybe you aren\'t an admin, or don\'t have the desired rights.`')

@bot.on(events.NewMessage(outgoing=True,pattern='^.set '))
async def update_bio(e):
    bio = e.text.split(' ', 1)[1]
    if len(bio) > 70:
        await e.edit('```Your Bio text is too long. The limit is 70 characters```')
    else:
        await bot(UpdateProfileRequest(
            about=bio
            ))
        await e.edit('```Succesfully edited Bio```')

@bot.on(events.NewMessage(outgoing=True,pattern='^.name '))
async def update_name(e):
    text = e.text.split(' ', 1)[1]
    name = text.split('\\n', 1)
    firstName = name[0]
    lastName = ' '
    if len(name) == 2:
        lastName = name[1]

    await bot(UpdateProfileRequest(
        first_name=firstName,
        last_name=lastName
        ))
    await e.edit('```Your name was succesfully changed```')


@bot.on(events.NewMessage(outgoing=True,pattern='^.uname '))
async def update_username(e):
    text = e.text.split(' ', 1)[1]
    allowed_char = re.match(r"[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", text)
    if not allowed_char:
        await e.edit('```Invalid Username```')
    elif len(text) > 30:
        await e.edit('```Your username is too long. The limit is 30 characters```')
    elif len(text) < 5:
        await e.edit('```Your username is to short.```')
    else:
        try:
            await bot(UpdateUsernameRequest(text))
            await e.edit('```Your username was succesfully changed```')
        except UsernameOccupiedError:
            await e.edit('```This username is already taken```')

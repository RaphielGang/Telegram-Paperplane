import io
import re

from telethon import TelegramClient, events
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.channels import EditPhotoRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (MessageEntityMentionName, MessageMediaDocument,
                               MessageMediaPhoto)
from telethon.utils import get_input_location

from userbot import bot

# ====================== CONSTANT ===============================
INVALID_MEDIA = "```The extension of the media entity is invalid.```"
PP_CHANGED = "```Profile Picture Changed```"
PP_TOO_SMOL = "```The image is too small```"
PP_ERROR = "```Failure while processing image```"

CHAT_PP_CHANGED = "```Chat Picture Changed```"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe you aren't an admin,`" \
                "`or don't have the desired rights.`"

BIO_LONG = "```Your Bio text is too long. The limit is 70 characters```"
BIO_SUCCESS = "```Succesfully edited Bio```"

INVALID_NAME = "```Invalid Username```"
NAME_OK = "```Your name was succesfully changed```"
USERNAME_TOO_LONG = "```Your username is too long. The limit is 30 characters```"
USERNAME_TOO_SHORT = "```Your username is to short.```"
USERNAME_SUCCESS = "```Your username was succesfully changed```"
USERNAME_TAKEN = "```This username is already taken```"
#===============================================================

@bot.on(events.NewMessage(outgoing=True, pattern="^.ppic$"))
async def profile_pic(ppic):
    if not ppic.text[0].isalpha() and ppic.text[0] not in ("/", "#", "@", "!"):
        message = await ppic.get_reply_message()
        photo = None
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.photo
                photo = await bot.download_media(message=photo)
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document.mime_type in ["image/jpeg", "image/png"]:
                    photo = message.media.document
                    photo = await bot.download_file(photo, file="propic.jpeg")
                    photo = io.BytesIO(photo)
                    photo.name = "image.jpeg"  # small hack for documents images
            else:
                await ppic.edit(INVALID_MEDIA)

        if photo:
            file = await bot.upload_file(photo)
            try:
                await bot(UploadProfilePhotoRequest(file))
                await ppic.edit(PP_CHANGED)

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await ppic.edit(PP_TOO_SMOL)
                elif isinstance(exc, ImageProcessFailedError):
                    await ppic.edit(PP_ERROR)


@bot.on(events.NewMessage(outgoing=True, pattern="^.xpic$"))
async def profile_photo(ppht):
    if not ppht.text[0].isalpha() and ppht.text[0] not in ("/", "#", "@", "!"):
        message = await ppht.get_reply_message()
        photo = None
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.photo
                photo = await bot.download_media(message=photo)
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document.mime_type in ["image/jpeg", "image/png"]:
                    photo = message.media.document
                    photo = await bot.download_file(photo, file="propic.jpeg")
                    photo = io.BytesIO(photo)
                    photo.name = "image.jpeg"  # small hack for documents images
            else:
                await ppht.edit(INVALID_MEDIA)

        if photo:
            file = await bot.upload_file(photo)
            try:
                await bot(EditPhotoRequest(e.chat_id, file))
                await ppht.edit(CHAT_PP_CHANGED)

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await ppht.edit(PP_TOO_SMOL)
                elif isinstance(exc, ImageProcessFailedError):
                    await ppht.edit(PP_ERROR)
                else:
                    await ppht.edit(CHAT_PP_ERROR)


@bot.on(events.NewMessage(outgoing=True, pattern="^.set "))
async def update_bio(e):
    bio = e.text.split(" ", 1)[1]
    if len(bio) > 70:
        await e.edit(BIO_LONG)
    else:
        await bot(UpdateProfileRequest(about=bio))
        await e.edit(BIO_SUCCESS)


@bot.on(events.NewMessage(outgoing=True, pattern="^.name "))
async def update_name(e):
    text = e.text.split(" ", 1)[1]
    name = text.split("\\n", 1)
    firstname = name[0]
    lastname = " "
    if len(name) == 2:
        lastname = name[1]

    await bot(UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await e.edit(NAME_OK)


@bot.on(events.NewMessage(outgoing=True, pattern="^.uname "))
async def update_username(updtusrnm):
    text = updtusrnm.text.split(" ", 1)[1]
    allowed_char = re.match(r"[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", text)
    if not allowed_char:
        await updtusrnm.edit(INVALID_NAME)
    elif len(text) > 30:
        await updtusrnm.edit(
            USERNAME_TOO_LONG
            )
    elif len(text) < 5:
        await updtusrnm.edit(
            USERNAME_TOO_SHORT
            )
    else:
        try:
            await bot(UpdateUsernameRequest(text))
            await updtusrnm.edit(USERNAME_SUCCESS)
        except UsernameOccupiedError:
            await updtusrnm.edit(USERNAME_TAKEN)

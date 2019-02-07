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
                await ppic.edit("```The extension of the media entity is invalid.```")

        if photo:
            file = await bot.upload_file(photo)
            try:
                await bot(UploadProfilePhotoRequest(file))
                await ppic.edit("```Profile Picture Changed```")

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await ppic.edit("```The image is too small```")
                elif isinstance(exc, ImageProcessFailedError):
                    await ppic.edit("```Failure while processing image```")


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
                await ppht.edit(
                    "```The extension of the media entity is invalid.```"
                    )

        if photo:
            file = await bot.upload_file(photo)
            try:
                await bot(EditPhotoRequest(e.chat_id, file))
                await ppht.edit("```Chat Picture Changed```")

            except Exception as exc:
                if isinstance(exc, PhotoCropSizeSmallError):
                    await ppht.edit("```The image is too small```")
                elif isinstance(exc, ImageProcessFailedError):
                    await ppht.edit("```Failure while processing image```")
                else:
                    await ppht.edit(
                        "`Some issue with updating the pic,`"
                        "`maybe you aren't an admin,`"
                        "`or don't have the desired rights.`"
                    )


@bot.on(events.NewMessage(outgoing=True, pattern="^.set "))
async def update_bio(e):
    bio = e.text.split(" ", 1)[1]
    if len(bio) > 70:
        await e.edit(
            "```Your Bio text is too long. The limit is 70 characters```"
            )
    else:
        await bot(UpdateProfileRequest(about=bio))
        await e.edit("```Succesfully edited Bio```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.name "))
async def update_name(e):
    text = e.text.split(" ", 1)[1]
    name = text.split("\\n", 1)
    firstname = name[0]
    lastname = " "
    if len(name) == 2:
        lastname = name[1]

    await bot(UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await e.edit("```Your name was succesfully changed```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.uname "))
async def update_username(updtusrnm):
    text = updtusrnm.text.split(" ", 1)[1]
    allowed_char = re.match(r"[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", text)
    if not allowed_char:
        await updtusrnm.edit("```Invalid Username```")
    elif len(text) > 30:
        await updtusrnm.edit(
            "```Your username is too long. The limit is 30 characters```"
            )
    elif len(text) < 5:
        await updtusrnm.edit(
            "```Your username is to short.```"
            )
    else:
        try:
            await bot(UpdateUsernameRequest(text))
            await updtusrnm.edit("```Your username was succesfully changed```")
        except UsernameOccupiedError:
            await updtusrnm.edit("```This username is already taken```")

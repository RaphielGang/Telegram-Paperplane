# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for changing your Telegram profile details. """

from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import UsernameOccupiedError, PhotoExtInvalidError
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import MessageMediaPhoto

from userbot import bot, HELPER
from userbot.events import register


# ====================== CONSTANT ===============================
INVALID_MEDIA = "```The extension of the media entity is invalid.```"
PP_CHANGED = "```Profile picture changed successfully.```"
PP_TOO_SMOL = "```This image is too small, use a bigger image.```"
PP_ERROR = "```Failure occured while processing image.```"

BIO_SUCCESS = "```Successfully edited Bio.```"

NAME_OK = "```Your name was succesfully changed.```"
USERNAME_SUCCESS = "```Your username was succesfully changed.```"
USERNAME_TAKEN = "```This username is already taken.```"
#===============================================================

@register(outgoing=True, pattern="^.name")
async def update_name(name):
    """ For .name command, change your name in Telegram. """
    if not name.text[0].isalpha() and name.text[0] not in ("/", "#", "@", "!"):
        newname = name.text[6:]
        if(" " not in newname):
            firstname = newname
            lastname = ""
        else:
            namesplit = newname.split(" ")
            firstname = namesplit[0]
            lastname = namesplit[1]

        await bot(UpdateProfileRequest(
            first_name=firstname,
            last_name=lastname))
        await name.edit(NAME_OK)

@register(outgoing=True, pattern="^.profilepic$")
async def set_profilepic(propic):
    """ For .profilepic command, change your profile picture in Telegram. """
    if not propic.text[0].isalpha() and propic.text[0] not in ("/", "#", "@", "!"):
        replymsg = await propic.get_reply_message()
        photo = None
        if replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await bot.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split('/'):
                photo = await bot.download_file(replymsg.media.document)
            else:
                await propic.edit(INVALID_MEDIA)

        if photo:
            try:
                await bot(UploadProfilePhotoRequest(
                    await bot.upload_file(photo)
                    ))
                await propic.edit(PP_CHANGED)
            except PhotoCropSizeSmallError:
                await propic.edit(PP_TOO_SMOL)
            except ImageProcessFailedError:
                await propic.edit(PP_ERROR)
            except PhotoExtInvalidError:
                await propic.edit(INVALID_MEDIA)


@register(outgoing=True, pattern="^.setbio (.*)")
async def set_biograph(setbio):
    """ For .setbio command, set a new bio for your profile in Telegram. """
    if not setbio.text[0].isalpha() and setbio.text[0] not in ("/", "#", "@", "!"):
        newbio = setbio.pattern_match.group(1)
        await bot(UpdateProfileRequest(about=newbio))
        await setbio.edit(BIO_SUCCESS)


@register(outgoing=True, pattern="^.username (.*)")
async def update_username(username):
    """ For .username command, set a new username in Telegram. """
    if not username.text[0].isalpha() and username.text[0] not in ("/", "#", "@", "!"):
        newusername = username.pattern_match.group(1)
        try:
            await bot(UpdateUsernameRequest(newusername))
            await username.edit(USERNAME_SUCCESS)
        except UsernameOccupiedError:
            await username.edit(USERNAME_TAKEN)

HELPER.update({
    "username": ".username <new_username>\
    \nUsage: Changes your Telegram username."
})
HELPER.update({
    "name": ".name <firstname> or .name <firstname> <lastname>\
    \nUsage: Changes your Telegram name.\
    \n(First and last name will get split by a space)"
})
HELPER.update({
    "profilepic": ".profilepic\
    \nUsage: Reply with .profilepic to an image to change \
your Telegram profie picture."
})
HELPER.update({
    "setbio": ".setbio <new_bio>\
    \nUsage: Changes your Telegram bio."
})

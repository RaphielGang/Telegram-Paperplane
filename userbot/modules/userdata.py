# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for changing your Telegram profile details. """

import time
import os

from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import (PhotoExtInvalidError,
                                          UsernameOccupiedError)
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          GetUserPhotosRequest,
                                          UploadProfilePhotoRequest)
from telethon.tl.types import InputPhoto, MessageMediaPhoto, Channel, User, Chat

from userbot import CMD_HELP, bot
from userbot.utils import inline_mention
from userbot.events import register

# ====================== CONSTANT ===============================
INVALID_MEDIA = "```The extension of the media entity is invalid.```"
PP_CHANGED = "```Profile picture changed successfully.```"
PP_TOO_SMOL = "```This image is too small, use a bigger image.```"
PP_ERROR = "```Failure occured while processing image.```"

BIO_SUCCESS = "```Successfully edited Bio.```"

NAME_OK = "```Your name was successfully changed.```"
USERNAME_SUCCESS = "```Your username was successfully changed.```"
USERNAME_TAKEN = "```This username is already taken.```"
# ===============================================================


@register(outgoing=True, pattern="^.name")
async def update_name(name):
    """ For .name command, change your name in Telegram. """
    newname = name.text[6:]
    if " " not in newname:
        firstname = newname
        lastname = ""
    else:
        namesplit = newname.split(" ", 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    await bot(UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await name.edit(NAME_OK)


@register(outgoing=True, pattern="^.profilepic$")
async def set_profilepic(propic):
    """ For .profilepic command, change your profile picture in Telegram. """
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
            await bot(UploadProfilePhotoRequest(await bot.upload_file(photo)))
            os.remove(photo)
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
    newbio = setbio.pattern_match.group(1)
    await bot(UpdateProfileRequest(about=newbio))
    await setbio.edit(BIO_SUCCESS)


@register(outgoing=True, pattern="^.username (.*)")
async def update_username(username):
    """ For .username command, set a new username in Telegram. """
    newusername = username.pattern_match.group(1)
    try:
        await bot(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@register(outgoing=True, pattern=r"^.delpfp")
async def remove_profilepic(delpfp):
    """ For .delpfp command, delete your current
        profile picture in Telegram. """
    group = delpfp.text[8:]
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await bot(
        GetUserPhotosRequest(user_id=delpfp.from_id,
                             offset=0,
                             max_id=0,
                             limit=lim))
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(id=sep.id,
                       access_hash=sep.access_hash,
                       file_reference=sep.file_reference))
    await bot(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(
        f"`Successfully deleted {len(input_photos)} profile picture(s).`")


@register(outgoing=True, pattern=f'^.stats')
async def stats(event: NewMessage.Event) -> None:  # pylint: disable = R0912, R0914, R0915
    """Command to get stats about the account"""
    waiting_message = await event.edit('Collecting stats. This might take a while.')
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    largest_group_member_count = 0
    largest_group_with_admin = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity

        if isinstance(entity, Channel):
            # participants_count = (await event.get_participants(dialog,
            # limit=0)).total
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1

            elif entity.megagroup:
                groups += 1
                # if participants_count > largest_group_member_count:
                #     largest_group_member_count = participants_count
                if entity.creator or entity.admin_rights:
                    # if participants_count > largest_group_with_admin:
                    #     largest_group_with_admin = participants_count
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1

        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1

        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1

        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time

    full_name = inline_mention(await event.client.get_me())
    response = f'**Stats for {full_name}** \n'
    response += f'    **Private Chats:** {private_chats} \n'
    response += f'        **Users:** {private_chats - bots} \n'
    response += f'        **Bots:** {bots} \n'
    response += f'    **Groups:** {groups} \n'
    response += f'    **Channels:** {broadcast_channels} \n'
    response += f'    **Admin in Groups:** {admin_in_groups} \n'
    response += f'        **Creator:** {creator_in_groups} \n'
    response += f'        **Admin Rights:** {admin_in_groups - creator_in_groups} \n'
    response += f'    **Admin in Channels:** {admin_in_broadcast_channels} \n'
    response += f'        **Creator:** {creator_in_channels} \n'
    response += f'        **Admin Rights:** {admin_in_broadcast_channels - creator_in_channels} \n'
    response += f'    **Unread:** {unread} \n'
    response += f'    **Unread Mentions:** {unread_mentions} \n\n'
    response += f'__Took:__ {stop_time:.02f}s \n'

    await event.edit(response)


CMD_HELP.update(
    {
        "userdata": [
            'Userdata',
            " - `username` <new_username>: Change your Telegram username.\n"
            " - `name` <firstname> or name <firstname> <lastname>: Change your Telegram name.\n"
            " - `profilepic`: Change your Telegram avatar with the replied photo.\n"
            " - `setbio` <new_bio>: Change your Telegram bio.\n"
            " - `delpfp` or delpfp <number>/<all>: Delete your Telegram avatar(s).\n"
            " - `stats`: Get some basic Telegram stats about yourself.\n\n"
            "**All commands can be used with** `.`"]})

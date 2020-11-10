# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""
Get Telegram Profile Picture and other information
and set as own profile.
"""

# Credits of Plugin @ViperAdnan and @mrconfused(revert)[will add sql soon]

import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from userbot import ALIVE_NAME, BOTLOG_CHATID, DEFAULT_BIO, BOTLOG, TEMP_DOWNLOAD_DIRECTORY, CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^\.clone ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(
        user_id, TEMP_DOWNLOAD_DIRECTORY
    )
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await bot(functions.account.UpdateProfileRequest(first_name=first_name))
    await bot(functions.account.UpdateProfileRequest(last_name=last_name))
    await bot(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await bot.upload_file(profile_pic)  # pylint:disable=E060
    await bot(
        functions.photos.UploadProfilePhotoRequest(pfile)  # pylint:disable=E0602
    )
    await event.delete()
    await bot.send_message(
        event.chat_id, "**LET US BE AS ONE**", reply_to=reply_message
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#CLONED\nSuccesfulley cloned [{first_name}](tg://user?id={user_id })",
        )


@register(outgoing=True, pattern="^\.revert$")
async def _(event):
    if event.fwd_from:
        return
    name = f"{ALIVE_NAME}"
    bio = f"{DEFAULT_BIO}"
    n = 1
    await bot(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=n)
        )
    )
    await bot(functions.account.UpdateProfileRequest(about=bio))
    await bot(functions.account.UpdateProfileRequest(first_name=name))
    await event.edit("succesfully reverted to your account back")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"#REVERT\nSuccesfully reverted back to your profile"
        )


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
        return replied_user, None
    input_str = None
    try:
        input_str = event.pattern_match.group(1)
    except IndexError as e:
        return None, e
    if event.message.entities is not None:
        mention_entity = event.message.entities
        probable_user_mention_entity = mention_entity[0]
        if isinstance(probable_user_mention_entity, MessageEntityMentionName):
            user_id = probable_user_mention_entity.user_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        try:
            user_object = await event.client.get_entity(input_str)
            user_id = user_object.id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    if event.is_private:
        try:
            user_id = event.chat_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    try:
        user_object = await event.client.get_entity(int(input_str))
        user_id = user_object.id
        replied_user = await event.client(GetFullUserRequest(user_id))
        return replied_user, None
    except Exception as e:
        return None, e


CMD_HELP.update(
    {
        "fake acc": [
            'Fake Acc', " - `.clone`: reply to user who you want to clone the profile.\n"
            " - `revert: Reverts back to your profile.\n\n"
            "**All commands can be used with** `.`"]})

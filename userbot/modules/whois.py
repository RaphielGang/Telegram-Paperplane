# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'whois' which is MPL
# License: MPL and OSSRPL
""" Userbot module for getiing info about any user on Telegram(including you!). """

import os

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from userbot import HELPER
from userbot.events import register

TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")


@register(pattern=".whois ?(.*)", outgoing=True)
async def who(event):
    """ For .whois command, get info about a user. """
    if event.fwd_from:
        return

    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    photo, caption = await fetch_info(replied_user, event)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    await event.client.send_file(
        event.chat_id,
        photo,
        caption=caption,
        link_preview=False,
        force_document=False,
        reply_to=message_id_to_reply,
        parse_mode="html"
    )

    if not photo.startswith("http"):
        os.remove(photo)

    await event.delete()


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
            else:
                # the disgusting CRAP way, of doing the thing
                try:
                    user_object = await event.client.get_entity(user)
                    replied_user = await event.client(GetFullUserRequest(user_object.id))
                except (TypeError, ValueError) as err:
                    await event.edit(str(err))
                    return None
        else:
            try:
                user_object = await event.client.get_entity(user)
                replied_user = await event.client(GetFullUserRequest(user_object.id))
            except (TypeError, ValueError) as err:
                await event.edit(str(err))
                return None

    return replied_user

async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about

    try:
        photo = await event.client.download_profile_photo(
            user_id,
            TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
            download_big=True
        )
    except TypeError:
        photo = "https://thumbs.dreamstime.com/b/no-user-profile-picture-24185395.jpg"

    if first_name:
        first_name = first_name.replace("\u2060", "")
    else:
        first_name = "This User has no First Name"
    if last_name:
        last_name = last_name.replace("\u2060", "")
    else:
        last_name = "This User has no Last Name"
    if username:
        username = "@{}".format(username)
    else:
        username = "This User has no Username"
    if user_bio:
        user_bio = user_bio
    else:
        user_bio = "This User has no About"

    caption = "<b>USER INFO:</b> \n"
    caption += f"First Name: {first_name} \n"
    caption += f"Last Name: {last_name} \n"
    caption += f"Username: {username} \n"
    caption += f"ID: <code>{user_id}</code> \n \n"
    caption += f"Bio: \n<code>{user_bio}</code> \n \n"
    caption += f"Common Chats with this user: {common_chat} \n"
    caption += f"Permanent Link To Profile: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"

    return photo, caption

HELPER.update({
    "whois": ".whois <username> or reply to someones text with .whois\
    \nUsage: Gets info of an user."
})
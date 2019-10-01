# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting info
    about any user on Telegram(including you!). """

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from userbot import CMD_HELP
from userbot.events import register


@register(pattern="^.info(?: |$)(.*)", outgoing=True)
async def info(usr):
    """ For .whois command, get info about a user. """
    if not usr.fwd_from:

        tofind = await get_user(usr)

        try:
            caption = await fetch_info(tofind, usr)
        except AttributeError:
            usr.edit("User Doesn't Exist!")
            return

        await usr.edit(caption, parse_mode="html")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    first_name = first_name.replace(
        "\u2060", "") if first_name else ("This User has no First Name")
    last_name = last_name.replace(
        "\u2060", "") if last_name else ("This User has no Last Name")
    username = "@{}".format(username) if username else (
        "This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio

    if user_id == (await event.client.get_me()).id:
        common_chat = "I've seen them in... Wow. Are they stalking me? "
        common_chat += "They're in all the same places I am... oh. It's me."
    else:
        common_chat = replied_user.common_chats_count

    caption = "</b>User Info:</b>\n" \
              f"First Name: {first_name} \n" \
              f"Last Name: {last_name} \n" \
              f"Username: {username} \n" \
              f"Is Bot: {is_bot} \n" \
              f"Is Restricted: {restricted} \n" \
              f"Is Verified by Telegram: {verified} \n" \
              f"ID: <code>{user_id}</code> \n \n" \
              f"Bio: \n<code>{user_bio}</code> \n \n" \
              f"Common Chats with this user: {common_chat} \n" \
              f"Permanent Link To Profile: " \
              f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"
    return caption


CMD_HELP.update({
    "info": ".info <username>(or reply to the target person's message)\n"
            "Usage: Get info about a user."})

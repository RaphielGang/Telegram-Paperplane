# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'whois' which is MPL
# License: MPL and OSSRPL
#
""" Userbot module for getiing info
    about any user on Telegram(including you!). """

import json
import os
import yaml
from html import escape

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from userbot import CMD_HELP
from userbot.events import register, grp_exclude
from userbot.modules.helpers import send_message_as_file

TMP_DOWNLOAD_DIRECTORY = "./"


@register(pattern=r"^.whois(?: |$)(.*)", outgoing=True)
@grp_exclude()
async def who(event):
    """For .whois command, get info about a user."""
    if event.fwd_from:
        return

    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    caption = await fetch_info(replied_user, event)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    await event.edit(caption, parse_mode="html")


async def get_user(event):
    """Get the user from argument or replied message."""
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
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("This User has no First Name")
    )
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("This User has no Last Name")
    )
    username = "@{}".format(username) if username else ("This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio

    if user_id != (await event.client.get_me()).id:
        common_chat = replied_user.common_chats_count
    else:
        common_chat = "I've seen them in... Wow. Are they stalking me? "
        common_chat += "They're in all the same places I am... oh. It's me."

    caption = "<b>USER INFO:</b> \n"
    caption += f"First Name: {first_name} \n"
    caption += f"Last Name: {last_name} \n"
    caption += f"Username: {username} \n"
    caption += f"Is Bot: {is_bot} \n"
    caption += f"Is Restricted: {restricted} \n"
    caption += f"Is Verified by Telegram: {verified} \n"
    caption += f"ID: <code>{user_id}</code> \n \n"
    caption += f"Bio: \n<code>{user_bio}</code> \n \n"
    caption += f"Common Chats with this user: {common_chat} \n"
    caption += f"Permanent Link To Profile: "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'

    return caption


def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data

    if hasattr(obj, "_ast"):
        return todict(obj._ast())

    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]

    if hasattr(obj, "__dict__"):
        data = {
            key: todict(value, classkey)
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith("_")
        }
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data

    return obj


@register(pattern=r"^.raw(?: |$)(.*)", outgoing=True)
@grp_exclude()
async def msg_info(event):
    arg = event.pattern_match.group(1) or "yaml"
    reply = await event.get_reply_message()

    if not reply:
        return await event.edit("`Reply message missing! Can't get raw data.`")

    if arg not in ["obj", "json", "yaml"]:
        await event.edit("`Wrong argument! Supported arguments are: yaml, obj, json.`")

    if arg == "obj":
        res_txt = f"{reply}"
    elif arg == "json":
        res_txt = json.dumps(todict(reply), indent=4, default=str)
    elif arg == "yaml":
        res_txt = yaml.dump(todict(reply), default_style="", sort_keys=False)

    if len(res_txt) > 4096:
        return await send_message_as_file(event, res_txt)

    return await event.edit(f"<code>{escape(res_txt)}</code>", parse_mode="html")


CMD_HELP.update(
    {
        "whois": [
            "Whois",
            " - `.whois <username>`: Get info about the target (argument or reply) user.\n",
            " - `.raw <yaml|json|obj>: Get the raw Message object of the replied message. "
            "If no argument is specified, the YAML format is used.\n",
        ]
    }
)

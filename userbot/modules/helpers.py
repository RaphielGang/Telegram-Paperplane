# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""
Helper functions to be used in modules
"""

import struct
from telethon.tl.types import MessageEntityMention, MessageEntityMentionName


async def get_user_from_event(event):
    """Get the user from argument or replied message."""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        return user_obj

    user = event.pattern_match.group(1)
    user_obj = None
    if not user:
        return False

    if user.isnumeric():
        user = int(user)

    entity = user
    if event.message.entities is not None:
        (
            prob_user_mention_entity,
            prob_user_mention_text,
        ) = event.message.get_entities_text()[0]

        if isinstance(prob_user_mention_entity, MessageEntityMentionName):
            entity = prob_user_mention_entity.user_id
        elif isinstance(prob_user_mention_entity, MessageEntityMention):
            entity = prob_user_mention_text

    try:
        user_obj = await event.client.get_entity(entity)
    except (TypeError, ValueError, struct.error, OverflowError):
        return False

    return user_obj


async def get_user_and_reason_from_event(event):
    user_obj = await get_user_from_event(event)

    if event.reply_to_msg_id:
        reason = event.pattern_match.group(1)
    else:
        reason = event.pattern_match.group(2)

    return (user_obj, reason)


async def get_user_from_id(user, event):
    """Getting user from user ID"""
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj

from re import findall, match
from typing import List

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (MessageEntityMentionName,
                               ChannelParticipantsAdmins,
                               ChannelParticipantsBots, MessageEntityMention, InputPeerChannel, InputPeerChat)


def parse_arguments(message: str, valid: List[str]) -> (dict, str):
    options = {}

    # Handle boolean values
    for opt in findall(r'([.!]\S+)', message):
        if opt[1:] in valid:
            if opt[0] == '.':
                options[opt[1:]] = True
            elif opt[0] == '!':
                options[opt[1:]] = False
            message = message.replace(opt, '')

    # Handle key/value pairs
    for opt in findall(r'(\S+):(?:"([\S\s]+)"|(\S+))', message):
        key, val1, val2 = opt
        value = val2 or val1[1:-1]
        if key in valid:
            if value.isnumeric():
                value = int(value)
            elif match(r'[Tt]rue|[Ff]alse', value):
                match(r'[Tt]rue', value)
            options[key] = value
            message = message.replace(f"{key}:{value}", '')

    return options, message.strip()


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d


def extract_urls(message):
    matches = findall(r'(https?://\S+)', str(message))
    return list(matches)


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


async def get_user_from_event(event: NewMessage.Event, **kwargs):
    """ Get the user from argument or replied message. """
    reply_msg: Message = await event.get_reply_message()
    user = kwargs.get('user', None)

    if user:
        # First check for a user id
        if user.isnumeric():
            user = int(user)

        # Then check for a user mention (@username)
        elif event.message.entities is not None:
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
            return None

    # Check for a forwarded message
    elif (reply_msg and
          reply_msg.forward and
          reply_msg.forward.sender_id and
          kwargs['forward']):
        forward = reply_msg.forward
        replied_user = await event.client(GetFullUserRequest(forward.sender_id))

    # Check for a replied to message
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))

    # Last case scenario is to get the current user
    else:
        self_user = await event.client.get_me()
        replied_user = await event.client(GetFullUserRequest(self_user.id))

    return replied_user


async def get_chat_from_event(event: NewMessage.Event, **kwargs):
    reply_msg: Message = await event.get_reply_message()
    chat = kwargs.get('chat', None)

    if chat:
        try:
            input_entity = await event.client.get_input_entity(chat)
            if isinstance(input_entity, InputPeerChannel):
                return await event.client(GetFullChannelRequest(input_entity.channel_id))
            elif isinstance(input_entity, InputPeerChat):
                return await event.client(GetFullChatRequest(input_entity.chat_id))
            else:
                return None
        except(TypeError, ValueError):
            return None
    # elif reply_msg and reply_msg.forward:
    #     return None
    else:
        chat = await event.get_chat()
        return await event.client(GetFullChannelRequest(chat.id))


async def list_admins(event):
    adms = await event.client.get_participants(event.chat, filter=ChannelParticipantsAdmins)
    adms = map(lambda x: x if not x.bot else None, adms)
    adms = [i for i in list(adms) if i]
    return adms


async def list_bots(event):
    bots = await event.client.get_participants(event.chat, filter=ChannelParticipantsBots)
    return bots


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = ' '.join(names)
    return full_name

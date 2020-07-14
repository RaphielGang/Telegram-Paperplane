# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting info
    about any user on Telegram(including you!). """

from telethon.events import NewMessage

from userbot import CMD_HELP, spamwatch
from userbot.events import register
from userbot.utils import parse_arguments, get_user_from_event
from userbot.utils.tgdoc import *


@register(pattern=r"^\.u(?:ser)?(\s+[\S\s]+|$)", outgoing=True)
async def who(event: NewMessage.Event):
    """ For .user command, get info about a user. """
    if event.fwd_from:
        return

    args, user = parse_arguments(event.pattern_match.group(1), [
        'id', 'forward', 'general', 'bot', 'misc', 'all', 'mention'
    ])

    args['forward'] = args.get('forward', True)
    args['user'] = user

    replied_user = await get_user_from_event(event, **args)

    if not replied_user:
        await event.edit("**Failed to get information for user**")
        return

    user_info = await fetch_info(replied_user, **args)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        pass

    await event.edit(str(user_info), parse_mode="markdown")


async def fetch_info(replied_user, **kwargs):
    """ Get details from the User object. """
    user = replied_user.user

    id_only = kwargs.get('id', False)
    show_general = kwargs.get('general', True)
    show_bot = kwargs.get('bot', False)
    show_misc = kwargs.get('misc', False)
    show_all = kwargs.get('all', False)
    mention_name = kwargs.get('mention', False)

    if show_all:
        show_general = True
        show_bot = True
        show_misc = True

    full_name = str(user.first_name + ' ' + (user.last_name or ''))

    if mention_name:
        title = Link(full_name, f'tg://user?id={user.id}')
    else:
        title = Bold(full_name)

    if id_only:
        return KeyValueItem(title, Code(user.id))

    general = SubSection(
        Bold('general'), KeyValueItem(
            'id', Code(
                user.id)), KeyValueItem(
            'first_name', Code(
                user.first_name)), KeyValueItem(
            'last_name', Code(
                user.last_name)), KeyValueItem(
            'username', Code(
                user.username)), KeyValueItem(
            'mutual_contact', Code(
                user.mutual_contact)), KeyValueItem(
            'common groups', Code(
                replied_user.common_chats_count)))

    if spamwatch:
        banobj = spamwatch.get_ban(user.id)
        if banobj:
            general.items.append(
                KeyValueItem(
                    'gbanned',
                    f'True / {banobj.reason}'))
        else:
            general.items.append(KeyValueItem('gbanned', 'False'))

    bot = SubSection(Bold('bot'),
                     KeyValueItem('bot', Code(user.bot)),
                     KeyValueItem('bot_chat_history', Code(user.bot_chat_history)),
                     KeyValueItem('bot_info_version', Code(user.bot_info_version)),
                     KeyValueItem('bot_inline_geo', Code(user.bot_inline_geo)),
                     KeyValueItem('bot_inline_placeholder',
                                  Code(user.bot_inline_placeholder)),
                     KeyValueItem('bot_nochats', Code(user.bot_nochats)))

    misc = SubSection(
        Bold('misc'), KeyValueItem(
            'restricted', Code(
                user.restricted)), KeyValueItem(
            'restriction_reason', Code(
                user.restriction_reason)), KeyValueItem(
            'deleted', Code(
                user.deleted)), KeyValueItem(
            'verified', Code(
                user.verified)), KeyValueItem(
            'min', Code(
                user.min)), KeyValueItem(
            'lang_code', Code(
                user.lang_code)))

    return Section(title,
                   general if show_general else None,
                   misc if show_misc else None,
                   bot if show_bot else None)


CMD_HELP.update({"user info": ['User Info',
                               " - `u(ser) [options] (username|id)` Or, in response to a message `.u(ser) [options]`:"
                               " List information about a particular user.\n\n"
                               "**Options:**\n\n"
                               "`.id`: Show only the user's ID\n"
                               "`.general`: Show general user info\n"
                               "`.bot`: Show bot related info\n"
                               "`.misc`: Show miscelanious info\n"
                               "`.all`: Show all info (overrides other options)\n"
                               "`.mention`: Inline mention the user\n"
                               "`.forward`: Follow forwarded message\n\n"
                               "**All commands can be used with** `.`"]
                 })

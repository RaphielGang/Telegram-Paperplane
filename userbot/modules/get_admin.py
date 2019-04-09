# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'adminlist' which is MPL
# License: MPL and OSSRPL

""" Userbot module allowing you to get the admin list in a chat. """

from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantsAdmins
from userbot import HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.adminlist$")
async def get_admin(show):
    """ For .adminlist command, list all of the admins of the chat. """
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = f'<b>Admins in {title}:</b> \n'
        try:
            async for user in show.client.iter_participants(
                    show.chat_id, filter=ChannelParticipantsAdmins
            ):
                if not user.deleted:
                    link =f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    ID = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {ID}"
                else:
                    mentions += f"\nDeleted Account <code>{user.id}</code>"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        await show.edit(mentions, parse_mode="html")

HELPER.update({
    "adminlist": ".adminlist\
    \nUsage: Retrieves all admins in the chat."
})
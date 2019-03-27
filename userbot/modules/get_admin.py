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


@register(outgoing=True, pattern="^.adminlist")
async def get_admin(show):
    """ For .adminlist command, list all of the admins of the chat. """
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        mentions = "Admins in {}: \n".format(show.chat.title or "this chat")
        try:
            async for user in show.client.iter_participants(
                    show.chat_id, filter=ChannelParticipantsAdmins
            ):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        await show.edit(mentions)

HELPER.update({
    "adminlist <parmeter>": "Retrieves all admins, if parameter is 0, tags them, if its 1."
})

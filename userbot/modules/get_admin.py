# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'adminlist' which is MPL
# License: MPL and OSSRPL

""" Userbot module allowing you to get the admin list in a chat. """

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from userbot import HELPER
from userbot.events import register

banned_rights = ChatBannedRights(
            until_date=None,
            view_messages=True,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            embed_links=True,
        )

unbanned_rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
            )


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


@register(outgoing=True, pattern="^.delusers ?(.*)")
async def get_admin(show):
    """ For .adminlist command, list all of the admins of the chat. """
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        con = show.pattern_match.group(1)
        del_u = 0
        del_status = "`No deleted accounts found, Group is cleaned as Hell`"

        if not show.is_group:
            await show.edit("`This command is only for groups!`")
            return

        if con != "clean":
            await show.edit("`Searching for zombie accounts...`")
            async for user in show.client.iter_participants(
                    show.chat_id
            ):
                if user.deleted:
                    del_u += 1

            if del_u > 0:
                del_status = f"`found`  **{del_u}**  `deleted account(s) in this group\nclean them by using .delusers clean`"
            await show.edit(del_status)
            return

        # Here laying the sanity check
        chat = await show.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # Well
        if not admin and not creator:
            await show.edit("`You aren't an admin here!`")
            return

        await show.edit("`Cleaning deleted accounts...`")
        del_u = 0
        del_a = 0

        async for user in show.client.iter_participants(
                    show.chat_id
            ):
            if user.deleted:
                try:
                    await show.client(
                        EditBannedRequest(
                            show.chat_id,
                            user.id,
                            banned_rights
                        )
                    )
                except UserAdminInvalidError:
                    del_u -= 1
                    del_a += 1
                await show.client(
                        EditBannedRequest(
                            show.chat_id,
                            user.id,
                            unbanned_rights
                        )
                    )
                del_u += 1

        if del_u > 0:
            del_status = f"`cleaned`  **{del_u}**  `deleted account(s)`"

        if del_a > 0:
            del_status = f"`cleaned`  **{del_u}**  `deleted account(s)`\n**{del_a}**  `deleted admin accounts are not removed`"

        await show.edit(del_status)


HELPER.update({
    "adminlist": ".adminlist\
    \nUsage: Retrieves all admins in the chat."
})

HELPER.update({
    'delusers': '.delusers\
\nUsage: Searches for deleted accounts in a group.\
\n\n.delusers clean\
\nUsage: Searches and removes deleted accounts from the group'
})

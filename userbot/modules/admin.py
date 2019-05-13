# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
"""
Userbot module which has commands related to and requiring admin privileges to use
"""

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)

from userbot import BRAIN_CHECKER, HELPER, LOGGER, LOGGER_GROUP, bot
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`You aren't an admin!`"
NO_PERM = "`You don't have sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe you aren't an admin,`" \
                "`or don't have the desired rights.`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
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

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)
# ================================================


@register(outgoing=True, pattern="^.setgrouppic$")
async def set_group_photo(gpic):
    """ For .setgrouppic command, changes the picture of a group """
    if not gpic.text[0].isalpha() and gpic.text[0] not in ("/", "#", "@", "!"):
        replymsg = await gpic.get_reply_message()
        chat = await gpic.get_chat()
        photo = None

        if not chat.admin_rights or chat.creator:
            await gpic.edit(NO_ADMIN)
            return

        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await bot.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split('/'):
                photo = await bot.download_file(replymsg.media.document)
            else:
                await gpic.edit(INVALID_MEDIA)

        if photo:
            try:
                await EditPhotoRequest(
                    gpic.chat_id,
                    await bot.upload_file(photo)
                )
                await gpic.edit(CHAT_PP_CHANGED)

            except PhotoCropSizeSmallError:
                await gpic.edit(PP_TOO_SMOL)
            except ImageProcessFailedError:
                await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
async def promote(promt):
    """ For .promote command, do promote targeted person """
    if not promt.text[0].isalpha() \
            and promt.text[0] not in ("/", "#", "@", "!"):
        # Get targeted chat
        chat = await promt.get_chat()
        # Grab admin status or creator in a chat
        admin = chat.admin_rights
        creator = chat.creator

        # If not admin and not creator, also return
        if not admin and not creator:
            await promt.edit(NO_ADMIN)
            return

        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True
        )

        await promt.edit("`Promoting...`")

        user = await get_user(promt)
        if user:
            pass
        else:
            return

        # Try to promote if current user is admin or creator
        try:
            await promt.client(
                EditAdminRequest(
                    promt.chat_id,
                    user.id,
                    new_rights
                )
            )
            await promt.edit("`Promoted Successfully!`")

        # If Telethon spit BadRequestError, assume
        # we don't have Promote permission
        except BadRequestError:
            await promt.edit(NO_PERM)
            return

        # Announce to the logging group if we have promoted successfully
        if LOGGER:
            await promt.client.send_message(
                LOGGER_GROUP,
                "#PROMOTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {promt.chat.title}(`{promt.chat_id}`)"
            )


@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ For .demote command, do demote targeted person """
    if not dmod.text[0].isalpha() and dmod.text[0] not in ("/", "#", "@", "!"):
        # Admin right check
        chat = await dmod.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        if not admin and not creator:
            await dmod.edit(NO_ADMIN)
            return

        # If passing, declare that we're going to demote
        await dmod.edit("`Demoting...`")

        user = await get_user(dmod)
        if user:
            pass
        else:
            return

        # New rights after demotion
        newrights = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None
        )
        # Edit Admin Permission
        try:
            await dmod.client(
                EditAdminRequest(
                    dmod.chat_id,
                    user.id,
                    newrights
                )
            )

        # If we catch BadRequestError from Telethon
        # Assume we don't have permission to demote
        except BadRequestError:
            await dmod.edit(NO_PERM)
            return
        await dmod.edit("`Demoted Successfully!`")

        # Announce to the logging group if we have demoted successfully
        if LOGGER:
            await dmod.client.send_message(
                LOGGER_GROUP,
                "#DEMOTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)"
            )


@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
async def thanos(bon):
    """ For .ban command, do "thanos" at targeted person """
    if not bon.text[0].isalpha() and bon.text[0] not in ("/", "#", "@", "!"):
        # Here laying the sanity check
        chat = await bon.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # Well
        if not admin and not creator:
            await bon.edit(NO_ADMIN)
            return

        user = await get_user(bon)
        if user:
            pass
        else:
            return

        # If the user is a sudo
        if user.id in BRAIN_CHECKER:
            await bon.edit(
                "`Ban Error! I am not supposed to ban this user`"
            )
            return

        # Announce that we're going to whack the pest
        await bon.edit("`Whacking the pest!`")

        try:
            await bon.client(
                EditBannedRequest(
                    bon.chat_id,
                    user.id,
                    BANNED_RIGHTS
                )
            )
        except BadRequestError:
            await bon.edit(NO_PERM)
            return
        # Helps ban group join spammers more easily
        try:
            reply = await bon.get_reply_message()
            if reply:
                await reply.delete()
        except BadRequestError:
            await bon.edit("`I dont have message nuking rights! But still he was banned!`")
            return
        # Delete message and then tell that the command
        # is done gracefully
        # Shout out the ID, so that fedadmins can fban later

        await bon.edit("`{}` was banned!".format(str(user.id)))

        # Announce to the logging group if we have demoted successfully
        if LOGGER:
            await bon.client.send_message(
                LOGGER_GROUP,
                "#BAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {bon.chat.title}(`{bon.chat_id}`)"
            )


@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ For .unban command, undo "thanos" on target """
    if not unbon.text[0].isalpha() and unbon.text[0] \
            not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
        )

        # Here laying the sanity check
        chat = await unbon.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # Well
        if not admin and not creator:
            await unbon.edit(NO_ADMIN)
            return

        # If everything goes well...
        await unbon.edit("`Unbanning...`")

        user = await get_user(unbon)
        if user:
            pass
        else:
            return

        try:
            await unbon.client(EditBannedRequest(
                unbon.chat_id,
                user.id,
                rights
            ))
            await unbon.edit("```Unbanned Successfully```")

            if LOGGER:
                await unbon.client.send_message(
                    LOGGER_GROUP,
                    "#UNBAN\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)"
                )
        except UserIdInvalidError:
            await unbon.edit("`Uh oh my unban logic broke!`")


@register(outgoing=True, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
    """
    This function is basically muting peeps
    """
    if not spdr.text[0].isalpha() and spdr.text[0] not in ("/", "#", "@", "!"):
        # Check if the function running under SQL mode
        try:
            from userbot.modules.sql_helper.spam_mute_sql import mute
        except AttributeError:
            await spdr.edit(NO_SQL)
            return

        # Admin or creator check
        chat = await spdr.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await spdr.edit(NO_ADMIN)
            return

        user = await get_user(spdr)
        if user:
            pass
        else:
            return

        # If the targeted user is a Sudo
        if user.id in BRAIN_CHECKER:
            await spdr.edit(
                "`Mute Error! I am not supposed to mute this user`"
            )
            return

        # If everything goes well, do announcing and mute
        await spdr.edit("`Gets a tape!`")
        mute(spdr.chat_id, user.id)

        # Announce that the function is done
        await spdr.edit("`Safely taped!`")

        # Announce to logging group
        if LOGGER:
            await spdr.client.send_message(
                LOGGER_GROUP,
                "#MUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)"
            )


@register(outgoing=True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ For .unmute command, unmute the target """
    if not unmot.text[0].isalpha() and unmot.text[0] \
            not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
        )

        # Admin or creator check
        chat = await unmot.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await unmot.edit(NO_ADMIN)
            return

        # Check if the function running under SQL mode
        try:
            from userbot.modules.sql_helper.spam_mute_sql import unmute
        except AttributeError:
            await unmot.edit(NO_SQL)
            return

        # If admin or creator, inform the user and start unmuting
        await unmot.edit('```Unmuting...```')
        user = await get_user(unmot)
        if user:
            pass
        else:
            return

        unmute(unmot.chat_id, user.id)

        try:
            await unmot.client(
                EditBannedRequest(
                    unmot.chat_id,
                    user.id,
                    rights
                )
            )
            await unmot.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")
            return

        if LOGGER:
            await unmot.client.send_message(
                LOGGER_GROUP,
                "#UNMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)"
            )


@register(incoming=True)
async def muter(moot):
    """ Used for deleting the messages of muted people """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(EditBannedRequest(
                    moot.chat_id,
                    moot.sender_id,
                    rights
                ))
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@register(outgoing=True, pattern="^.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """ For .ungmute command, ungmutes the target in the userbot """
    if not un_gmute.text[0].isalpha() and un_gmute.text[0] \
            not in ("/", "#", "@", "!"):
        # Admin or creator check
        chat = await un_gmute.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await un_gmute.edit(NO_ADMIN)
            return

        # Check if the function running under SQL mode
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except AttributeError:
            await un_gmute.edit(NO_SQL)

        user = await get_user(un_gmute)
        if user:
            pass
        else:
            return

        # If pass, inform and start ungmuting
        await un_gmute.edit('```Ungmuting...```')

        ungmute(user.id)

        # Inform about success
        await un_gmute.edit("```Ungmuted Successfully```")

        if LOGGER:
            await un_gmute.client.send_message(
                LOGGER_GROUP,
                "#UNGMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {un_gmute.chat.title}(`{un_gmute.chat_id}`)"
            )


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ For .gmute command, gmutes the target in the userbot """
    if not gspdr.text[0].isalpha() and gspdr.text[0] not in ("/", "#", "@", "!"):
        # Admin or creator check
        chat = await gspdr.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await gspdr.edit(NO_ADMIN)
            return

        # Check if the function running under SQL mode
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except AttributeError:
            await gspdr.edit(NO_SQL)
            return

        user = await get_user(gspdr)
        if user:
            pass
        else:
            return

        # If the targeted user is a SUDO
        if user.id in BRAIN_CHECKER:
            await gspdr.edit("`Gmute Error! Couldn't gmute this user`")
            return

        # If pass, inform and start gmuting
        await gspdr.edit("`Grabs a huge, sticky duct tape!`")
        gmute(user.id)

        # Delete the replied message and inform about success
        await gspdr.delete()
        await gspdr.respond("`Globally taped!`")

        if LOGGER:
            await gspdr.client.send_message(
                LOGGER_GROUP,
                "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)"
            )


@register(outgoing=True, pattern="^.delusers(?: |$)(.*)")
async def rm_deletedacc(show):
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
                del_status = f"found **{del_u}** deleted account(s) in this group \
                \nclean them by using .delusers clean"
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
                            BANNED_RIGHTS
                        )
                    )
                except ChatAdminRequiredError:
                    await show.edit("`you don't have ban rights in this group`")
                    return
                except UserAdminInvalidError:
                    del_u -= 1
                    del_a += 1
                await show.client(
                    EditBannedRequest(
                        show.chat_id,
                        user.id,
                        UNBAN_RIGHTS
                    )
                )
                del_u += 1

        if del_u > 0:
            del_status = f"cleaned **{del_u}** deleted account(s)"

        if del_a > 0:
            del_status = f"cleaned **{del_u}** deleted account(s) \
            \n**{del_a}** deleted admin accounts are not removed"

        await show.edit(del_status)


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
                    link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nDeleted Account <code>{user.id}</code>"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        await show.edit(mentions, parse_mode="html")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj

HELPER.update({
    "promote": "Usage: Reply to someone's message with .promote to promote them."
})
HELPER.update({
    "ban": "Usage: Reply to someone's message with .ban to ban them."
})
HELPER.update({
    "demote": "Usage: Reply to someone's message with .demote to revoke their admin permissions."
})
HELPER.update({
    "unban": "Usage: Reply to someone's message with .unban to unban them in this chat."
})
HELPER.update({
    "mute": "Usage: Reply to someone's message with .mute to mute them, works on admins too"
})
HELPER.update({
    "unmute": "Usage: Reply to someone's message with .unmute to remove them from muted list."
})
HELPER.update({
    "gmute": "Usage: Reply to someone's message with .gmute to mute them in all \
groups you have in common with them."
})
HELPER.update({
    "ungmute": "Usage: Reply someone's message with .ungmute to remove them from the gmuted list."
})

HELPER.update(
    {
        "delusers": "Usage: Searches for deleted accounts in a group."
    }
)

HELPER.update(
    {
        "delusers clean": "Usage: Searches and removes deleted accounts from the group"
    }
)

HELPER.update(
    {
        "adminlist" : "Usage: Retrieves all admins in the chat."
    }
)

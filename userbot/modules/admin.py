# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

"""Userbot module to help you manage a group"""

from asyncio import sleep

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ChatNotModifiedError, ImageProcessFailedError,
                             PhotoCropSizeSmallError, UserAdminInvalidError)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import (EditChatDefaultBannedRightsRequest,
                                            UpdatePinnedMessageRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`You aren't an admin!`"
NO_PERM = "`You don't have sufficient permissions!`"
NO_SQL = "`Database connections failing!`"

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

KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

CHATLOCK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    change_info=True,
    pin_messages=True
)

CHATUNLOCK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    send_polls=None,
    invite_users=True,
    change_info=True,
    pin_messages=True
)

# ================================================


@register(outgoing=True, group_only=True, pattern="^\.setgrouppic$")
async def set_group_photo(gpic):
    """For .setgrouppic command, changes the picture of a group"""
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
            await EditPhotoRequest(gpic.chat_id, await bot.upload_file(photo))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, group_only=True, pattern="^\.promote(?: |$)(.*)")
async def promote(promt):
    """For .promote command, do promote targeted person"""
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=admin.add_admins,
                                 invite_users=admin.invite_users,
                                 change_info=admin.change_info,
                                 ban_users=admin.ban_users,
                                 delete_messages=admin.delete_messages,
                                 pin_messages=admin.pin_messages)

    await promt.edit("`Promoting...`")

    user = await get_user_from_event(promt)
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, "Admin"))
        await promt.edit("`Promoted Successfully!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#PROMOTE\n"
                           f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, group_only=True, pattern="^\.demote(?: |$)(.*)")
async def demote(dmod):
    """For .demote command, do demote targeted person"""
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Demoting...`")

    user = await get_user_from_event(dmod)
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Edit Admin Permission
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, "Admin"))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Demoted Successfully!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#DEMOTE\n"
                           f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, group_only=True, pattern="^\.ban(?: |$)(.*)")
async def ban(bon):
    """For .ban command, do a ban at targeted person"""
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Whacking the pest!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BadRequestError:
        await bon.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        bmsg = "`I dont have enough rights! But still he was banned!`"
        await bon.edit(bmsg)
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later

    await bon.edit("`{}` was banned!".format(str(user.id)))

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
                           f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, group_only=True, pattern="^\.unban(?: |$)(.*)")
async def nothanos(unbon):
    """For .unban command, unban the target"""
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

    user = await get_user_from_event(unbon)
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Unbanned Successfully```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                               f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                               f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)")
    except UserIdInvalidError:
        await unbon.edit("`Uh oh my unban logic broke!`")


@register(outgoing=True, group_only=True, pattern="^\.delusers(?: |$)(.*)")
async def rm_deletedacc(show):
    """For .delusers command, clean deleted accounts."""
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "`No deleted accounts found, Group is cleaned as Hell`"

    if con != "clean":
        await show.edit("`Searching for zombie accounts...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)

        if del_u > 0:
            del_status = f"Found **{del_u}** deleted account(s) in this group,\
            \nclean them by using `.delusers clean`"

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

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("`You don't have enough rights.`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
            await sleep(1)
    if del_u > 0:
        del_status = f"cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"cleaned **{del_u}** deleted account(s) \
\n**{del_a}** deleted admin accounts are not removed"

    await show.edit(del_status)


@register(outgoing=True, group_only=True, pattern="^\.adminlist$")
async def get_admin(show):
    """For .adminlist command, list all of the admins of the chat."""
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>Admins in {title}:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link_unf = "<a href=\"tg://user?id={}\">{}</a>"
                link = link_unf.format(user.id, user.first_name)
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, group_only=True, pattern="^\.pin(?: |$)(.*)")
async def pin(msg):
    """The .pin pins the replied to message at the top of the chat."""
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Reply to a message which you want to pin.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True
    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Pinned Successfully!`")

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
                           f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
                           f"LOUD: {not is_silent}")


@register(outgoing=True, group_only=True, pattern="^\.kick(?: |$)(.*)")
async def kick(usr):
    """For .kick command, kick someone from the group using the userbot."""
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Couldn't fetch user.`")
        return

    await usr.edit("`Kicking...`")

    try:
        await usr.client(EditBannedRequest(usr.chat_id, user.id, KICK_RIGHTS))
        await sleep(.5)
    except BadRequestError:
        await usr.edit(NO_PERM)
        return
    await usr.client(
        EditBannedRequest(usr.chat_id, user.id,
                          ChatBannedRights(until_date=None)))

    kmsg = "`Kicked` [{}](tg://user?id={})`!`"
    await usr.edit(kmsg.format(user.first_name, user.id))

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
                           f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, group_only=True, pattern="^\.lock$")
async def emergency_lock(lock):
    """For emergency-locking a chat"""
    # Admin or creator check
    chat = await lock.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await lock.edit(NO_ADMIN)
        return

    await lock.edit("`Locking...`")

    try:
        await lock.client(
            EditChatDefaultBannedRightsRequest(
                lock.chat_id,
                CHATLOCK_RIGHTS
            ))
        await lock.edit("`Locked!`")
    except ChatNotModifiedError:
        await lock.edit("`Chat has already been locked!`")

    if BOTLOG:
        await lock.client.send_message(
            BOTLOG_CHATID, "#LOCK\n"
            f"CHAT: {lock.chat.title}(`{lock.chat_id}`)"
        )


@register(outgoing=True, group_only=True, pattern="^\.unlock$")
async def chat_unlock(unlock):
    """For unlocking a chat"""
    # Admin or creator check
    chat = await unlock.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await unlock.edit(NO_ADMIN)
        return

    await unlock.edit("`Unlocking...`")

    try:
        await unlock.client(
            EditChatDefaultBannedRightsRequest(
                unlock.chat_id,
                CHATUNLOCK_RIGHTS
            ))
        await unlock.edit("`Unlocked!`")
    except ChatNotModifiedError:
        await unlock.edit("`Chat already unlocked`")

    if BOTLOG:
        await unlock.client.send_message(
            BOTLOG_CHATID, "#UNLOCK\n"
            f"CHAT: {unlock.chat.title}(`{unlock.chat_id}`)"
        )


async def get_user_from_event(event):
    """Get the user from argument or replied message"""
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

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj


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


CMD_HELP.update(
    {
        "admins": [
            'Admins',
            " - `promote`: Promotes a user. Reply to the user or use their username/ID.\n"
            " - `demote`: Demotes an admin. Reply to the admin or use their username/ID.\n"
            " - `ban`: Bans a user. Reply to the user or use their username/ID.\n"
            " - `unban`: Unbans a user. Reply to the user or use their username/ID.\n"
            " - `delusers`: Searches for deleted accounts in a group/channel.\n"
            " - `delusers clean`: Searches for and kicks deleted accounts from a group/channel.\n"
            " - `adminlist`: Retrieves all admins in the chat.\n"
            " - `lock`: Lock current chat, allowing read only for non-admins.\n"
            " - `unlock`: Unlock current chat, allowing read/write for non-admins.\n\n"
            "**All commands can be used with** `.`"]})

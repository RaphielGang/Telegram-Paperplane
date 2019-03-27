# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
"""
Userbot module which has commands related to and requiring admin privileges to use
"""

from time import sleep

from telethon.errors import (BadRequestError, ImageProcessFailedError,
                             PhotoCropSizeSmallError)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChatAdminRights, ChatBannedRights,
                               MessageMediaPhoto)

from userbot import (BRAIN_CHECKER, LOGGER, LOGGER_GROUP, HELPER, bot)
from userbot.events import register

#=================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`You aren't an admin!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe you aren't an admin,`" \
                "`or don't have the desired rights.`"
INVALID_MEDIA = "`Invalid Extension`"
#================================================


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


@register(outgoing=True, pattern="^.promote$")
async def promote(promt):
    """ For .promote command, do promote targeted person """
    if not promt.text[0].isalpha() \
            and promt.text[0] not in ("/", "#", "@", "!"):
        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True
        )

        # Self explanatory
        if not await promt.get_reply_message():
            await promt.edit("`Give a reply message`")
        else:
            await promt.edit("`Promoting...`")

        # Try to promote if current user is admin or creator
        try:
            await promt.client(
                EditAdminRequest(promt.chat_id,
                                 (await promt.get_reply_message()).sender_id,
                                 new_rights)
            )
            await promt.edit("`Promoted Successfully!`")

        # If Telethon spit BadRequestError, assume
        # we don't have Promote permission
        except BadRequestError:
            await promt.edit(
                "`You Don't have sufficient permissions to parmod`"
                )
            return


@register(outgoing=True, pattern="^.demote$")
async def demote(dmod):
    """ For .demote command, do demote targeted person """
    if not dmod.text[0].isalpha() and dmod.text[0] not in ("/", "#", "@", "!"):
        # Get targeted chat
        chat = await dmod.get_chat()
        # Grab admin status or creator in a chat
        admin = chat.admin_rights
        creator = chat.creator

        # If there's no reply, return
        if not await dmod.get_reply_message():
            await dmod.edit("`Give a reply message`")
            return
        # If not admin and not creator, also return
        if not admin and not creator:
            await dmod.edit("`You aren't an admin!`")
            return

        # If passing, declare that we're going to demote
        await dmod.edit("`Demoting...`")

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
                EditAdminRequest(dmod.chat_id,
                                 (await dmod.get_reply_message()).sender_id,
                                 newrights)
            )

        # If we catch BadRequestError from Telethon
        # Assume we don't have permission to demote
        except BadRequestError:
            await dmod.edit(
                "`You Don't have sufficient permissions to demhott`"
                )
            return
        await dmod.edit("`Demoted Successfully!`")


@register(outgoing=True, pattern="^.ban$")
async def thanos(bon):
    """ For .ban command, do "thanos" at targeted person """
    if not bon.text[0].isalpha() and bon.text[0] not in ("/", "#", "@", "!"):
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

        # Here laying the sanity check
        chat = await bon.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # For dealing with reply-at-ban
        sender = await bon.get_reply_message()

        # Well
        if not admin and not creator:
            await bon.edit("`You aren't an admin!`")
            return

        # If the user is a sudo
        try:
            if sender.sender_id in BRAIN_CHECKER:
                await bon.edit(
                    "`Ban Error! I am not supposed to ban this user`"
                    )
                return

        # This exception handled if the user doesn't
        # Specifying any target (reply in this case)
        except AttributeError:
            await bon.edit("`You don't seems to do this right`")
            return

        # Announce that we're going to whacking the pest
        await bon.edit("`Whacking the pest!`")
        try:
            await bon.client(
                EditBannedRequest(
                    bon.chat_id,
                    sender.sender_id,
                    banned_rights
                )
            )
        except Exception:
            await bon.edit("`I couldn't ban this user! Possible reasons: \
                             Maybe the admin status was appointed by someone else.`")
            return
        # Helps ban group join spammers more easily
        try:
            await sender.delete()
        except Exception:
            await bon.edit("`I dont have message nuking rights! But still he was banned!`")
            return
        # Delete message and then tell that the command
        # is done gracefully
        # Shout out the ID, so that fedadmins can fban later

        await bon.edit("`{}` was banned!".format(str(sender.sender_id)))

        # Announce to the logging group if we done a banning
        if LOGGER:
            await bon.client.send_message(
                LOGGER_GROUP,
                "#BAN\n"
                "ID: `"+ str((await bon.get_reply_message()).sender_id)
                + "`",
            )


@register(outgoing=True, pattern="^.unban$")
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
        replymsg = await unbon.get_reply_message()
        try:
            await unbon.client(EditBannedRequest(
                unbon.chat_id,
                replymsg.sender_id,
                rights
                ))
            await unbon.edit("```Unbanned Successfully```")

            if LOGGER:
                await unbon.client.send_message(
                    LOGGER_GROUP,
                    "#UNBAN\n"
                    +"ID: `"+ str((await unbon.get_reply_message()).sender_id)
                    + "`",
                )
        except UserIdInvalidError:
            await unbon.edit("`Uh oh my unban logic broke!`")


@register(outgoing=True, pattern="^.mute$")
async def spider(spdr):
    """
    This function basically muting peeps
    """
    if not spdr.text[0].isalpha() and spdr.text[0] not in ("/", "#", "@", "!"):

        # If the targeted user is a Sudo
        if (await spdr.get_reply_message()).sender_id in BRAIN_CHECKER:
            await spdr.edit(
                "`Mute Error! I am not supposed to mute this user`"
                )
            return

        # Check if the function running under SQL mode
        try:
            from userbot.modules.sql_helper.spam_mute_sql import mute
        except AttributeError:
            await spdr.edit("`Running on Non-SQL mode!`")
            return

        # Get the targeted chat
        chat = await spdr.get_chat()
        # Check if current user is admin
        admin = chat.admin_rights
        # Check if current user is creator
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await spdr.edit("`You aren't an admin!`")
            return

        target = await spdr.get_reply_message()
        # Else, do announce and do the mute
        mute(spdr.chat_id, target.sender_id)
        await spdr.edit("`Gets a tape!`")

        # Announce that the function is done
        await spdr.edit("`Safely taped!`")

        # Announce to logging group
        if LOGGER:
            await spdr.client.send_message(
                LOGGER_GROUP,
                "#MUTE\n"
                +"ID: `"+ str((await spdr.get_reply_message()).sender_id)
                + "`",
            )


@register(outgoing=True, pattern="^.unmute$")
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
        replymsg = await unmot.get_reply_message()
        from userbot.modules.sql_helper.spam_mute_sql import unmute
        unmute(unmot.chat_id, replymsg.sender_id)
        try:
            await unmot.client(
                EditBannedRequest(
                    unmot.chat_id,
                    replymsg.sender_id,
                    rights
                )
            )
            await unmot.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")
        if LOGGER:
            await unmot.client.send_message(
                LOGGER_GROUP,
                "#MUTE\n"
                +"ID: `"+ str((await unmot.get_reply_message()).sender_id)
                + "`",
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

@register(outgoing=True, pattern="^.ungmute$")
async def ungmoot(un_gmute):
    """ For .ungmute command, ungmutes the target in the userbot """
    if not un_gmute.text[0].isalpha() and un_gmute.text[0] \
            not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except AttributeError:
            await un_gmute.edit('`Running on Non-SQL Mode!`')
        ungmute(str((await un_gmute.get_reply_message()).sender_id))
        await un_gmute.edit("```Ungmuted Successfully```")


@register(outgoing=True, pattern="^.gmute$")
async def gspider(gspdr):
    """ For .gmute command, gmutes the target in the userbot """
    if not gspdr.text[0].isalpha() and gspdr.text[0] not in ("/", "#", "@", "!"):
        if (await gspdr.get_reply_message()).sender_id in BRAIN_CHECKER:
            await gspdr.edit("`Mute Error! Couldn't mute this user`")
            return
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except AttributeError as err:
            await gspdr.edit("`Running on Non-SQL mode!`")
            return

        gmute(str((await gspdr.get_reply_message()).sender_id))
        await gspdr.edit("`Grabs a huge, sticky duct tape!`")
        sleep(5)
        await gspdr.delete()
        await gspdr.respond("`Taped!`")

        if LOGGER:
            await gspdr.send_message(
                LOGGER_GROUP,
                str((await gspdr.get_reply_message()).sender_id)
                + " was muted.",
            )

HELPER.update({
    "promote": "Usage: \nReply someone's message with .promote to promote them."
})
HELPER.update({
    "ban": "Usage: \nReply someone's message with .ban to ban them."
})
HELPER.update({
    "demote": "Usage: \nReply someone's message with .demote to revoke their admin permissions."
})
HELPER.update({
    "unban": "Usage: \nReply someone's message with .unban to unban them in this chat."
})
HELPER.update({
    "mute": "Usage: \nReply someone's message with .mute to mute them, works on admins too"
})
HELPER.update({
    "unmute": "Usage: \nReply someone's message with .unmute to remove them from muted list."
})
HELPER.update({
    "gmute": "Usage: \nReply someone's message with .gmute to mute them in all \
              groups you have in common with them."
})
HELPER.update({
    "ungmute": "Usage: \nReply someone's message with .ungmute to remove them from the gmuted list."
})

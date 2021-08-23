# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Paperplane module for kanging stickers or making new ones. """

import io
import math
import urllib.request
from PIL import Image

from telethon.tl.types import InputPeerNotifySettings, InputStickerSetID
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest

from userbot import CMD_HELP, bot
from userbot.events import register, grp_exclude

PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."
PACK_DOESNT_EXIST = "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."


@register(outgoing=True, pattern=r"^.kang($| )?(\W+?)? ?([0-9]*)?$")
@grp_exclude()
async def kang(event):
    """Function for .kang command, create a sticker pack and add stickers."""
    await event.edit("`Kanging...`")
    user = await bot.get_me()
    pack_username = ""
    if not user.username:
        try:
            user.first_name.decode("ascii")
            pack_username = user.first_name
        except UnicodeDecodeError:  # User's first name isn't ASCII, use ID instead
            pack_username = user.id
    else:
        pack_username = user.username

    textx = await event.get_reply_message()
    emoji = event.pattern_match.group(2)
    number = int(event.pattern_match.group(3) or 1)  # If no number specified, use 1
    new_pack = False

    if textx.photo or textx.sticker:
        message = textx
    elif event.photo or event.sticker:
        message = event
    else:
        await event.edit(
            "`You need to send/reply to a sticker/photo to be able to kang it!`"
        )
        return

    sticker = io.BytesIO()
    await bot.download_media(message, sticker)
    sticker.seek(0)

    if not sticker:
        await event.edit(
            "`Couldn't download sticker! Make sure you send a proper sticker/photo.`"
        )
        return

    is_anim = message.file.mime_type == "application/x-tgsticker"
    if not is_anim:
        img = await resize_photo(sticker)
        sticker.name = "sticker.png"
        sticker.seek(0)
        img.save(sticker, "PNG")

    # The user didn't specify an emoji...
    if not emoji:
        if message.file.emoji:  # ...but the sticker has one
            emoji = message.file.emoji
        else:  # ...and the sticker doesn't have one either
            emoji = "🤔"

    packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
    packtitle = (
        f"@{user.username or user.first_name}'s Paperplane Pack "
        f"{number}{' animated' if is_anim else ''}"
    )
    response = urllib.request.urlopen(
        urllib.request.Request(f"http://t.me/addstickers/{packname}")
    )
    htmlstr = response.read().decode("utf8").split("\n")
    new_pack = PACK_DOESNT_EXIST in htmlstr

    # Mute Stickers bot to ensure user doesn't get notification spam
    muted = await bot(
        UpdateNotifySettingsRequest(
            peer="t.me/Stickers",
            settings=InputPeerNotifySettings(mute_until=2 ** 31 - 1),
        )  # Mute forever
    )
    if not muted:  # Tell the user just in case, this may rarely happen
        await event.edit(
            "`Paperplane couldn't mute the Stickers bot, beware of notification spam.`"
        )

    if new_pack:
        await event.edit(
            "`This Paperplane Sticker Pack doesn't exist! Creating a new pack...`"
        )
        await newpack(is_anim, sticker, emoji, packtitle, packname)
    else:
        async with bot.conversation("t.me/Stickers") as conv:
            # Cancel any pending command
            await conv.send_message("/cancel")
            await conv.get_response()

            # Send the add sticker command
            await conv.send_message("/addsticker")
            await conv.get_response()

            # Send the pack name
            await conv.send_message(packname)
            x = await conv.get_response()

            # Check if the selected pack is full
            while x.text == PACK_FULL:
                # Switch to a new pack, create one if it doesn't exist
                number += 1
                packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
                packtitle = (
                    f"@{user.username or user.first_name}'s Paperplane Pack "
                    f"{number}{' animated' if is_anim else ''}"
                )

                await event.edit(
                    f"`Switching to Pack {number} due to insufficient space in Pack {number-1}.`"
                )

                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text == "Invalid pack selected.":  # That pack doesn't exist
                    await newpack(is_anim, sticker, emoji, packtitle, packname)

                    # Read all unread messages
                    await bot.send_read_acknowledge("t.me/Stickers")
                    # Unmute Stickers bot back
                    muted = await bot(
                        UpdateNotifySettingsRequest(
                            peer="t.me/Stickers",
                            settings=InputPeerNotifySettings(mute_until=None),
                        )
                    )

                    await event.edit(
                        f"`Sticker added to pack {number}{'(animated)' if is_anim else ''} with "
                        f"{emoji} as the emoji! "
                        f"This pack can be found `[here](t.me/addstickers/{packname})",
                        parse_mode="md",
                    )
                    return

            # Upload the sticker file
            if is_anim:
                upload = await message.client.upload_file(
                    sticker, file_name="AnimatedSticker.tgs"
                )
                await conv.send_file(upload, force_document=True)
            else:
                sticker.seek(0)
                await conv.send_file(sticker, force_document=True)
            await conv.get_response()

            # Send the emoji
            await conv.send_message(emoji)
            await conv.get_response()

            # Finish editing the pack
            await conv.send_message("/done")
            await conv.get_response()

    # Read all unread messages
    await bot.send_read_acknowledge("t.me/Stickers")
    # Unmute Stickers bot back
    muted = await bot(
        UpdateNotifySettingsRequest(
            peer="t.me/Stickers", settings=InputPeerNotifySettings(mute_until=None)
        )
    )

    await event.edit(
        f"`Sticker added to pack {number}{'(animated)' if is_anim else ''} with "
        f"{emoji} as the emoji! "
        f"This pack can be found `[here](t.me/addstickers/{packname})",
        parse_mode="md",
    )


@register(outgoing=True, pattern=r"^.kangpack($| )?([0-9]*)?$")
@grp_exclude()
async def kangpack(event):
    await event.edit("`Kanging the whole pack...`")
    user = await bot.get_me()
    pack_username = ""
    if not user.username:
        try:
            user.first_name.decode("ascii")
            pack_username = user.first_name
        except UnicodeDecodeError:  # User's first name isn't ASCII, use ID instead
            pack_username = user.id
    else:
        pack_username = user.username

    textx = await event.get_reply_message()

    if not textx.sticker:
        await event.edit(
            "`You need to reply to a sticker to be able to kang the whole pack!`"
        )
        return

    sticker_set = textx.file.sticker_set
    stickers = await event.client(
        GetStickerSetRequest(
            stickerset=InputStickerSetID(
                id=sticker_set.id, access_hash=sticker_set.access_hash
            )
        )
    )
    is_anim = textx.file.mime_type == "application/x-tgsticker"

    number = event.pattern_match.group(2) or 1
    new_pack = False
    while not new_pack:
        packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
        packtitle = (
            f"@{user.username or user.first_name}'s Paperplane Pack "
            f"{number}{' animated' if is_anim else ''}"
        )
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        new_pack = PACK_DOESNT_EXIST in htmlstr
        if not new_pack:
            if event.pattern_match.group(2):
                await event.edit(
                    "`This pack doesn't exist! Specify another number or omit the argument to let "
                    "Paperplane get the lowest available pack number automatically.`"
                )
                return
            number += 1

    # Mute Stickers bot to ensure user doesn't get notification spam
    muted = await bot(
        UpdateNotifySettingsRequest(
            peer="t.me/Stickers",
            settings=InputPeerNotifySettings(mute_until=2 ** 31 - 1),
        )  # Mute forever
    )
    if not muted:  # Tell the user just in case, this may rarely happen
        await event.edit(
            "`Paperplane couldn't mute the Stickers bot, beware of notification spam.`"
        )

    async with bot.conversation("Stickers") as conv:
        # Cancel any pending command
        await conv.send_message("/cancel")
        await conv.get_response()

        # Send new pack command
        if is_anim:
            await conv.send_message("/newanimated")
        else:
            await conv.send_message("/newpack")
        await conv.get_response()

        # Give the pack a name
        await conv.send_message(packtitle)
        await conv.get_response()

    for sticker in stickers.documents:
        async with bot.conversation("Stickers") as conv2:
            emoji = sticker.attributes[1].alt
            # Upload sticker file
            if is_anim:
                sticker_dl = io.BytesIO()
                await bot.download_media(sticker, sticker_dl)
                sticker_dl.seek(0)
                upload = await bot.upload_file(
                    sticker_dl, file_name="AnimatedSticker.tgs"
                )
                await conv2.send_file(upload, force_document=True)
            else:
                await conv2.send_file(sticker, force_document=True)
            await conv2.get_response()

            # Send the emoji
            await conv2.send_message(emoji)
            await conv2.get_response()

    async with bot.conversation("Stickers") as conv:
        # Publish the pack
        await conv.send_message("/publish")
        if is_anim:
            await conv.get_response()
            await conv.send_message(f"<{packtitle}>")
        await conv.get_response()

        # Skip pack icon selection
        await conv.send_message("/skip")
        await conv.get_response()

        # Send packname
        await conv.send_message(packname)
        await conv.get_response()

    # Read all unread messages
    await bot.send_read_acknowledge("t.me/Stickers")
    # Unmute Stickers bot back
    muted = await bot(
        UpdateNotifySettingsRequest(
            peer="t.me/Stickers", settings=InputPeerNotifySettings(mute_until=None)
        )
    )

    await event.edit(
        f"`Sticker pack {number}{' (animated)' if is_anim else ''} has been created!\n"
        f"It can be found` [here](t.me/addstickers/{packname})`.`",
        parse_mode="md",
    )


@register(outgoing=True, pattern=r"^.getsticker$")
@grp_exclude()
async def getsticker(event):
    await event.edit("`Getting the sticker as a file...`")
    textx = await event.get_reply_message()

    if not textx or not textx.sticker:
        await event.edit(
            "`You need to reply to a sticker to be able to get it as a file!`"
        )
        return

    sticker = io.BytesIO()
    await bot.download_media(textx, sticker)
    sticker.seek(0)

    if not sticker:
        await event.edit(
            "`Couldn't download the sticker! Make sure you reply to a proper sticker.`"
        )
        return

    if textx.file.mime_type == "application/x-tgsticker":
        upload = await event.client.upload_file(
            sticker, file_name="AnimatedSticker.tgs_"
        )
        await event.reply(
            file=upload,
            force_document=True,
            message="```Please rename the file manually to delete the _ from the extension "
            "(rename AnimatedSticker.tgs_ to AnimatedSticker.tgs). "
            "This is a Telegram limitation.```",
        )
    else:
        img = Image.open(sticker)
        sticker.name = "sticker.png"
        img.save(sticker, "PNG")
        sticker.seek(0)
        await event.reply(file=sticker, force_document=True)

    await event.edit("`Got the sticker as a file!`")


async def newpack(is_anim, sticker, emoji, packtitle, packname):
    async with bot.conversation("Stickers") as conv:
        # Cancel any pending command
        await conv.send_message("/cancel")
        await conv.get_response()

        # Send new pack command
        if is_anim:
            await conv.send_message("/newanimated")
        else:
            await conv.send_message("/newpack")
        await conv.get_response()

        # Give the pack a name
        await conv.send_message(packtitle)
        await conv.get_response()

        # Upload sticker file
        if is_anim:
            upload = await bot.upload_file(sticker, file_name="AnimatedSticker.tgs")
            await conv.send_file(upload, force_document=True)
        else:
            sticker.seek(0)
            await conv.send_file(sticker, force_document=True)
        await conv.get_response()

        # Send the emoji
        await conv.send_message(emoji)
        await conv.get_response()

        # Publish the pack
        await conv.send_message("/publish")
        if is_anim:
            await conv.get_response()
            await conv.send_message(f"<{packtitle}>")
        await conv.get_response()

        # Skip pack icon selection
        await conv.send_message("/skip")
        await conv.get_response()

        # Send packname
        await conv.send_message(packname)
        await conv.get_response()


async def resize_photo(photo):
    """Resize the given photo to 512x512"""
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


CMD_HELP.update(
    {
        "kang": [
            "Kang",
            " - `.kang <emoji> <number>`: Reply .kang to a sticker or an image to kang "
            "it to your Paperplane pack. Animated stickers are also supported.\n"
            "If emojis are sent, they will be used as the emojis for the sticker.\n"
            "If a number is sent, the emoji will be saved in the pack corresponding to that number. "
            "Otherwise, Paperplane will use an available pack name with the lowest number.\n"
            " - `.kangpack <number>`: Reply .kangpack to a sticker to kang the whole pack the sticker "
            "is in as a new Paperplane pack. The new pack will have all of the stickers from the "
            "kanged pack, with their corresponding emoji and order. Animated packs are also supported.\n"
            "If a number is sent, the emoji will be saved in the pack corresponding to that number. "
            "Otherwise, Paperplane will use an available pack name with the lowest number.\n"
            " - `.getsticker`: Reply .getsticker to a sticker to get it as a file! Animated "
            "sticker support is limited because of a Telegram limitation. Using the command with "
            "animated stickers will require you to rename the file to remove _ from the end of its"
            "extension.",
        ]
    }
)

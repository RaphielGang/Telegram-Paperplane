# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from userbot import LOGGER, LOGGER_GROUP, HELPER, WELCOME_MUTE, bot
from userbot.events import register
import asyncio
from userbot.modules.admin import BANNED_RIGHTS, UNBAN_RIGHTS
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)

from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)
from telethon import events
Spambot=False
@bot.on(events.ChatAction)
async def welcome_mute(welcm):
  if welcm.user_joined or welcm.user_added:
    from time import sleep
    sleep(10)
    if not WELCOME_MUTE:
        return
    async for message in bot.iter_messages(welcm.chat_id, from_user=welcm.action_message.from_id):
        global Spambot
        user = await welcm.client.get_entity(welcm.action_message.from_id)
        print(message.text)
        if "http://" in message.text:
            Spambot=True
        elif "t.me" in message.text:
            Spambot=True
        elif message.fwd_from:
            Spambot=True
        elif "https://" in message.text:
            Spambot=True
        else:
            if user.first_name in ("Bitmex", "Promotion", "Information", "Dex"):
                if user.last_name == "Bot":
                    Spambot=True
        break
    if Spambot:
        await welcm.reply("`Potential SpamBot Detected! Kicking away! Will log the ID for further purposes!`")
        chat = await welcm.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await welcm.reply("@admins \n`ANTI SPAMBOT DETECTOR! \nTHIS USER MATCHES MY ALGORITHMS AS A SPAMBOT!`")
            return
        try:
            await welcm.client(
                EditBannedRequest(
                    welcm.chat_id,
                    welcm.action_message.from_id,
                    BANNED_RIGHTS
                   )
             )
            await welcm.client(EditBannedRequest(
                welcm.chat_id,
                welcm.action_message.from_id,
                UNBAN_RIGHTS
                ))
        except:
            await welcm.reply("@admins \n`ANTI SPAMBOT DETECTOR! \nTHIS USER MATCHES MY ALGORITHMS AS A SPAMBOT!`")
            return
        await message.delete()
        await welcm.client.send_message(
                    LOGGER_GROUP,
                    "#SPAMBOT-KICK\n"
                    f"USER: [{user.first_name}](tg://user?id={welcm.action_message.from_id})\n"
                    f"CHAT: {welcm.chat.title}(`{welcm.chat_id}`)"
                )
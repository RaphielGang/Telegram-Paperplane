# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

''' A module for helping ban group join spammers. '''

from asyncio import sleep

from telethon.tl.functions.channels import EditBannedRequest
from telethon import events

from userbot import LOGGER, LOGGER_GROUP, HELPER, WELCOME_MUTE, bot
from userbot.modules.admin import BANNED_RIGHTS, UNBAN_RIGHTS


@bot.on(events.ChatAction)
async def welcome_mute(welcm):
    ''' Ban a recently joined user if it matches the spammer checking algorithm. '''
    if welcm.user_joined or welcm.user_added:
        users = []

        if welcm.user_added:
            for i in welcm.action_message.action.users:
                users.append(i)

        spambot = False

        await sleep(5)

        if not WELCOME_MUTE:
            return

        for user_id in users:
            async for message in bot.iter_messages(
                    welcm.chat_id,
                    from_user=user_id
            ):
                if not message: break
                
                join_time = welcm.action_message.date
                message_date = message.date

                if message_date < join_time:
                    continue # The message was sent before the user joined, thus ignore it

                ### DEBUGGING. LEAVING IT HERE FOR SOME TIME ###
                print(f"User Joined: {join_time}")
                print(f"Spam Message Sent: {message_date}")
                ###
                
                user = await welcm.client.get_entity(user_id)
                if "http://" in message.text:
                    spambot = True
                elif "t.me" in message.text:
                    spambot = True
                elif message.fwd_from:
                    spambot = True
                elif "https://" in message.text:
                    spambot = True
                else:
                    if user.first_name in (
                            "Bitmex",
                            "Promotion",
                            "Information",
                            "Dex",
                            "Announcements", 
                            "Info"
                    ):
                        if user.last_name == "Bot":
                            spambot = True

                if spambot:
                    print(f"Potential Spam Message: {message.text}")
                    await message.delete()
                    break

                continue # Check the next messsage

        if spambot:
            await welcm.reply(
                "`Potential Spambot Detected! Kicking away! "
                "Will log the ID for further purposes!\n"
                f"USER:` [{user.first_name}](tg://user?id={user.id})")

            chat = await welcm.get_chat()
            admin = chat.admin_rights
            creator = chat.creator
            if not admin and not creator:
                await welcm.reply(
                    "@admins\n"
                    "`ANTI SPAMBOT DETECTOR!\n"
                    "THIS USER MATCHES MY ALGORITHMS AS A SPAMBOT!`")
            else:
                try:
                    await welcm.client(
                        EditBannedRequest(
                            welcm.chat_id,
                            user.id,
                            BANNED_RIGHTS
                        )
                    )
                    await welcm.client(
                        EditBannedRequest(
                            welcm.chat_id,
                            user.id,
                            UNBAN_RIGHTS
                        )
                    )
                except:
                    await welcm.reply(
                        "@admins\n"
                        "`ANTI SPAMBOT DETECTOR!\n"
                        "THIS USER MATCHES MY ALGORITHMS AS A SPAMBOT!`")

            if LOGGER:
                await welcm.client.send_message(
                    LOGGER_GROUP,
                    "#SPAMBOT-KICK\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {welcm.chat.title}(`{welcm.chat_id}`)"
                )

HELPER.update({
    'welcome_mute': "If enabled in config.env or env var, \
        this module will ban(or inform admins) the group join \
        spammers if they match the userbot's algorithm of banning"
})

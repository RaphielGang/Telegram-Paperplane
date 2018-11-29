import os
from datetime import datetime
from telethon import TelegramClient, events
from telegraph import Telegraph, upload_file, exceptions
from userbot import bot
@bot.on(events.NewMessage(pattern=r".telegraph (media|text)", outgoing=True))
async def telegraph(event):
 if not e.text[0].isalpha():
    TMP_DOWNLOAD_DIRECTORY = os.getcwd()
    short_name = "baalajimaestro"
    PRIVATE_GROUP_BOT_API_ID = LOGGER_GROUP

    telegraph = Telegraph()
    r = telegraph.create_account(short_name=short_name)
    auth_url = r["auth_url"]
    if event.fwd_from:
        return
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        if LOGGER:
            await bot.send_message(
            PRIVATE_GROUP_BOT_API_ID,
            "Created New Telegraph account for the current session: {}. \n**Do not give this url to anyone, even if they say they are from Telegram!**".format(auth_url)
            )
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "media":
            downloaded_file_name = await bot.download_media(
                r_message,
                TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit("Downloaded to {} in {} seconds.".format(downloaded_file_name, ms))
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await event.edit("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await event.edit("Uploaded to https://telegra.ph/{} in {} seconds.".format(media_urls[0], (ms + ms_two)))
        elif input_str == "text":
            user_object = await bot.get_entity(r_message.from_id)
            title_of_page = user_object.first_name # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            page_content = r_message.message
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit("Pasted to https://telegra.ph/{} in {} seconds.".format(response["path"], ms))
    else:
        await event.edit("Reply to a message to get a permanent telegra.ph link. (Inspired by @ControllerBot)")

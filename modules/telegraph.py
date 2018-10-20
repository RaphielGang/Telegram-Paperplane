import os
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions


TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
short_name = os.environ.get("TELEGRAPH_SHORT_NAME", "BaalajiMaestro")
PRIVATE_GROUP_BOT_API_ID = borg.uid

telegraph = Telegraph()
r = telegraph.create_account(short_name=short_name)
auth_url = r["auth_url"]


@bot.on(events.NewMessage(pattern=r"\.telegraph (media|text)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    await bot.send_message(
        PRIVATE_GROUP_BOT_API_ID,
        "Created New Telegraph account {} for the current session. \n**Do not give this url to anyone, even if they say they are from Telegram!**".format(auth_url)
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

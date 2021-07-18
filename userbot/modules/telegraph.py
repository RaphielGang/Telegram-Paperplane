import time
from datetime import datetime

from telegraph import Telegraph, upload_file, exceptions

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register, grp_exclude

@register(pattern="(tgm|telegraph media)$", outgoing=True)
@grp_exclude()
async def telegraph(media):
    """Gives telegraph link of a given media.
       No text."""
    
    if not media.reply_to_msg_id:
        message = await media.edit("Reply to a media to get its telegraph link.")
        time.sleep(3)
        return await message.delete()
    
    
    await media.edit("Starting...")
    sttime = datetime.now()    

    Media = await media.get_reply_message()
    Downloaded = await media.client.download_media(Media)
    
    
    if not Media.media:
        message = await media.edit(
            "That doesn't look like "
            "a **media** to me."
        )
        time.sleep(5)
        return await message.delete()
    
    
    telegraph = Telegraph()
    account = telegraph.create_account(short_name="Paperplane")
    auth_url = account["auth_url"]
    
    if Media.file.ext not in (
        (
           [".jpg", ".jpeg", ".png", ".gif", ".mp4"]
        )
    ):
       await media.edit("I don't support this media.")
       return 
    
    await media.edit("Downloaded media.")
    time.sleep(0.5)
    
    await media.edit("Created telegraph account.")
    if BOTLOG:
        await media.client.send_message(
            BOTLOG_CHATID,
            "#TELEGRAPH\n"
            "Created an account in telegraph: \n"
            "[Account Link]"
            "("
            + auth_url
            + ")"
            "📗"
        ) 
    
    
    try:
      tlg_url = upload_file(Downloaded)
    except exceptions.TelegraphException as error:
      await media.edit("Oh no! I got an error.")
      time.sleep(1)
      await media.edit(
          "**REPORT**\n"
          f"`{str(error)}`"
      )
      return
    
    entime = datetime.now()
    time_passed = entime - sttime
    time_taken = time_passed.seconds
    
    await media.edit("• Your telegraph link is here: "
                     "[link]"
                    f"(https://telegra.ph{tlg_url[0]})"
                     "\n• Uploaded in "
                     f"{time_taken} secs."
               )
    

@register(pattern="(tgt|telegraph text)$", outgoing=True)
@grp_exclude()
async def telegraph(text):
    """Gives the telegraph link of text.
    No media."""
    
    if not text.reply_to_msg_id:
        message = await text.edit("Reply to a message to get its telegraph link.")
        time.sleep(3)
        return await message.delete()
    
    await text.edit("Starting...")
    sttime = datetime.now()
    
    Reply_Msg = await text.get_reply_message()
    Media = Reply_Msg.media
    Text = Reply_Msg.text
    
    Extention = None or Reply_Msg.file.ext
    if Extention in (
        (
           [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webp"]
        )
    ):
        Extention = False
        
    if Media:
        if Extention:
            message = await text.edit("Is it a file? I am downloading it...")
            Downloaded = await text.client.download_media(Reply_Msg)
            try:
                Content = (open(Downloaded)).read()
                Content = Content.replace("\n", "<br>")
            except:
                await text.edit("I couldn't make out any text in the file.")
                time.sleep(1)
                await text.edit("Lemme read the caption 🔍")
                time.sleep(1)
                Media = False
                                 
    elif not Media:
        if Text == "":
            message = await text.edit("I can't find any **text** around here.")
            time.sleep(3)
            return await message.delete()
        else:
            Content = Text.replace("\n", "<br>")
    
    
    telegraph = Telegraph()
    account = telegraph.create_account(short_name="Paperplane")
    auth_url = account["auth_url"]
    
    
    await text.edit("Created Telegraph account.")
    time.sleep(0.5)
    
    
    if BOTLOG:
        await text.client.send_message(
            BOTLOG_CHATID,
            "#TELEGRAPH\n"
            "Created an account in telegraph: \n"
            "[Account Link]"
            "("
            + auth_url
            + ")"
            "📗"
        ) 
    
    Page = telegraph.create_page("Paperplane", html_content=Content)
    
    entime = datetime.now()
    time_passed = entime - sttime
    time_taken = time_passed.seconds
    
    await text.edit("• Your telegraph link is here: "
                     "[link]"
                    f"(https://telegra.ph/{Page['path']})"
                     "\n• Uploaded in "
                     f"{time_taken} secs."
               )    
    
    
CMD_HELP.update(
    {
        "telegraph": [
            "Telegraph",
            "- `.telegraph media||.tgm`: Gives telegraph link for the replied media.\n"
            "    **Note:** Only [.jpg, .jpeg, .png, .gif, .mp4] file types are supported.\n"
            "-`.telegraph text||.tgt`: Writes replied text in telegraph page and returns link." 
        ]
    }
)

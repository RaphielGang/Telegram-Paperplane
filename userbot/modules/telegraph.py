import time
from datetime import datetime

from telegraph import Telegraph, upload_file, exceptions
from PIL import Image

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register, grp_exclude

@register(pattern=r"telegraph media|tgm", outgoing=True)
@grp_exclude()
async def telegraph(event):
    """Gives telegraph link of a given media.
       No text."""
    
    await event.edit("Starting...")
    
    media = await event.get_reply_message()
    downloaded = await event.client.download_media(media)
    
    await event.edit("Downloaded media.")
    
    telegraph = Telegraph()
    account = telegraph.create_account(short_name="Paperplane")
    auth_url = account["auth_url"]
    
    if media.file.ext != (
        (
            ".jpg" or ".jpeg" or ".png" or ".gif" or ".mp4"
        )
    ):
        await event.edit("I don't support that media.")
        return
    
    await event.edit("Created telegraph account.")
    if BOTLOG:
        await event.client.send_message(
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
      sttime = datetime.now()
      tlg_url = upload_file(downloaded)
    except exceptions.TelegraphException as error:
      await event.edit("Oh no! I got an error")
      time.sleep(1)
      await event.edit(str(error))
      return
    
    entime = datetime.now()
    time_passed = entime - sttime
    time_taken = time_passed.seconds
    
    await event.edit("• Your telegraph link is here: "
                     "[link]"
                     f"(https://telegra.ph{tlg_url[0]})"
                     "\n• Uploaded in "
                     f"{time_taken} secs."
               )
    
    

import time
from datetime import datetime

from telegraph import Telegraph, upload_file, exceptions

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register, grp_exclude

@register(pattern="t(?:elegraph|gm)$", outgoing=True)
@grp_exclude()
async def telegraph(media):
    """Gives telegraph link of a given media.
       No text."""
    
    await media.edit("Starting...")
    sttime = datetime.now()    

    Media = await media.get_reply_message()
    Downloaded = await media.client.download_media(Media)
    
    await media.edit("Downloaded media.")
    time.sleep(0.5)
    
    telegraph = Telegraph()
    account = telegraph.create_account(short_name="Paperplane")
    auth_url = account["auth_url"]
    
    if str(Downloaded).endswith != (
        (
            ".jpg" or ".jpeg" or ".png" or ".mp4" or ".gif"
        )
    ):
       await media.edit("I don't support this media.")
       return 
    
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
      await media.edit("Oh no! I got an error")
      time.sleep(1)
      await media.edit(str(error))
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
    

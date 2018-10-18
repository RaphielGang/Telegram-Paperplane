import asyncio
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont


download_directory = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")
font_file_to_use = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def progress(current, total):
    print("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@bot.on(events.NewMessage(pattern=r"\.getime ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    current_time = datetime.now().strftime("%H : %M : %S")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    required_file_name = download_directory + " " + str(datetime.now()) + ".webp"
    img = Image.new('RGB', (250, 50), color = (0, 0, 0))
    fnt = ImageFont.truetype(font_file_to_use, 30)
    d = ImageDraw.Draw(img)
    d.text((10,10), current_time, font=fnt, fill=(255,255,255))
    img.save(required_file_name)
    await bot.send_file(
        event.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
        progress_callback=progress
    )
    os.remove(required_file_name)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Created sticker in {} seconds".format(ms))
    await asyncio.sleep(5)
    await event.delete()


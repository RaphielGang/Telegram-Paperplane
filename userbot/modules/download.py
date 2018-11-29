import json
import os
import subprocess
import requests
import time
from userbot import LOGGER,LOGGER_GROUP
from telethon import TelegramClient, events
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError
from PIL import Image
from userbot import bot
TEMP_DOWNLOAD_DIRECTORY = os.getcwd()
def progress(current, total):
    print("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))
def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        else:
            output_lst.append(current_file_name)
    return output_lst
@bot.on(events.NewMessage(pattern=r"^.download (.*)", outgoing=True))
@bot.on(events.MessageEdited(pattern=r"^.download (.*)", outgoing=True))
async def downloader(event):
 if not e.text[0].isalpha():
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        downloaded_file_name = await bot.download_media(
            await event.get_reply_message(),
            TEMP_DOWNLOAD_DIRECTORY,
            progress_callback=progress
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        required_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
        start = datetime.now()
        r = requests.get(url, stream=True)
        with open(required_file_name, "wb") as fd:
            total_length = r.headers.get('content-length')
            # https://stackoverflow.com/a/15645088/4723940
            if total_length is None: # no content length header
                fd.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=128):
                    dl += len(chunk)
                    fd.write(chunk)
                    done = int(100 * dl / total_length)
                    download_progress_string = "Downloading ... [%s%s]" % ('=' * done, ' ' * (50-done))
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(required_file_name, ms))
    else:
        await event.edit("Reply to a message to download to my local server.")
@bot.on(events.NewMessage(pattern=r"^.upload (stream|vn|all) (.*)", outgoing=True))
@bot.on(events.MessageEdited(pattern=r"^.upload (stream|vn|all) (.*)", outgoing=True))
async def uploader(event):
 if not e.text[0].isalpha():
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    type_of_upload = event.pattern_match.group(1)
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    input_str = event.pattern_match.group(2)
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb_path = "a_random_f_file_name" + ".jpg"
        thumb = get_video_thumb(file_name, output=thumb_path)
    if os.path.exists(file_name):
        start = datetime.now()
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                await bot.send_file(
                    event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ],
                    progress_callback=progress
                )
            elif round_message:
                await bot.send_file(
                    event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=0,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True
                        )
                    ],
                    progress_callback=progress
                )
            elif spam_big_messages:
                await event.edit("TBD: Not (yet) Implemented")
                return
            end = datetime.now()
            ms = (end - start).seconds
            os.remove(thumb)
            await event.edit("Uploaded in {} seconds.".format(ms))
        except FileNotFoundError as e:
            await event.edit(str(e))
    else:
        await event.edit("404: File Not Found")

import asyncio
import json
import os
import subprocess
from datetime import datetime

import requests
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from telethon import events
from telethon.errors import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo

from userbot import LOGS, bot

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")


def progress(current, total):
    LOGS.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@bot.on(events.NewMessage(pattern=r".download ?(.*)", outgoing=True))
@bot.on(events.MessageEdited(pattern=r".download ?(.*)", outgoing=True))
async def download(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.fwd_from:
            return
        await e.edit("Processing ...")
        input_str = e.pattern_match.group(1)
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        if e.reply_to_msg_id:
            start = datetime.now()
            downloaded_file_name = await bot.download_media(
                await e.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            end = datetime.now()
            ms = (end - start).seconds
            await e.edit(
                "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )
        elif "|" in input_str:
            url, file_name = input_str.split("|")
            url = url.strip()
            # https://stackoverflow.com/a/761825/4723940
            file_name = file_name.strip()
            required_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
            start = datetime.now()
            r = requests.get(url, stream=True)
            with open(required_file_name, "wb") as fd:
                total_length = r.headers.get("content-length")
                # https://stackoverflow.com/a/15645088/4723940
                if total_length is None:  # no content length header
                    fd.write(r.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for chunk in r.iter_content(chunk_size=128):
                        dl += len(chunk)
                        fd.write(chunk)
                        done = int(100 * dl / total_length)
                        download_progress_string = "Downloading ... [%s%s]" % (
                            "=" * done,
                            " " * (50 - done),
                        )
                        LOGS.info(download_progress_string)
            end = datetime.now()
            ms = (end - start).seconds
            await e.edit(
                "Downloaded to `{}` in {} seconds.".format(required_file_name, ms)
            )
        else:
            await e.edit("Reply to a message to download to my local server.")


@bot.on(events.NewMessage(pattern=r".uploadir (.*)", outgoing=True))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.fwd_from:
            return
        input_str = e.pattern_match.group(1)
        if os.path.exists(input_str):
            start = datetime.now()
            await e.edit("Processing ...")
            lst_of_files = lst_of_files(input_str, [])
            LOGS.info(lst_of_files)
            u = 0
            await e.edit(
                "Found {} files. Uploading will start soon. Please wait!".format(
                    len(lst_of_files)
                )
            )
            for single_file in lst_of_files:
                if os.path.exists(single_file):
                    # https://stackoverflow.com/a/678242/4723940
                    caption_rts = os.path.basename(single_file)
                    if not caption_rts.lower().endswith(".mp4"):
                        await bot.send_file(
                            e.chat_id,
                            single_file,
                            caption=caption_rts,
                            force_document=False,
                            allow_cache=False,
                            reply_to=e.message.id,
                            progress_callback=progress,
                        )
                    else:
                        thumb_image = os.path.join(input_str, "thumb.jpg")
                        metadata = extractMetadata(createParser(single_file))
                        duration = 0
                        width = 0
                        height = 0
                        if metadata.has("duration"):
                            duration = metadata.get("duration").seconds
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                        await bot.send_file(
                            e.chat_id,
                            single_file,
                            caption=caption_rts,
                            thumb=thumb_image,
                            force_document=False,
                            allow_cache=False,
                            reply_to=e.message.id,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    round_message=False,
                                    supports_streaming=True,
                                )
                            ],
                            progress_callback=progress,
                        )
                    os.remove(single_file)
                    u = u + 1
            end = datetime.now()
            ms = (end - start).seconds
            await e.edit("Uploaded {} files in {} seconds.".format(u, ms))
        else:
            await e.edit("404: Directory Not Found")


@bot.on(events.NewMessage(pattern=r".upload (.*)", outgoing=True))
@bot.on(events.MessageEdited(pattern=r".upload (.*)", outgoing=True))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.fwd_from:
            return
        if e.is_channel and not e.is_group:
            await e.edit("`Uploading isn't permitted on channels`")
            return
        await e.edit("Processing ...")
        input_str = e.pattern_match.group(1)
        if input_str in ("userbot.session", "config.env"):
            await e.edit("`That's a dangerous operation! Not Permitted!`")
            return
        if os.path.exists(input_str):
            start = datetime.now()
            await bot.send_file(
                e.chat_id,
                input_str,
                force_document=True,
                allow_cache=False,
                reply_to=e.message.id,
                progress_callback=progress,
            )
            end = datetime.now()
            ms = (end - start).seconds
            await e.edit("Uploaded in {} seconds.".format(ms))
        else:
            await e.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)
            ),
            "-filter:v",
            "scale={}:-1".format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if not p.returncode and os.path.lexists(file):
        return output


def extract_w_h(file):
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warn(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@bot.on(events.NewMessage(pattern=r".uploadas(stream|vn|all) (.*)", outgoing=True))
async def _(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.fwd_from:
            return
        await e.edit("Processing ...")
        type_of_upload = e.pattern_match.group(1)
        supports_streaming = False
        round_message = False
        spam_big_messages = False
        if type_of_upload == "stream":
            supports_streaming = True
        if type_of_upload == "vn":
            round_message = True
        if type_of_upload == "all":
            spam_big_messages = True
        input_str = e.pattern_match.group(2)
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
                duration = metadata.get("duration").seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            try:
                if supports_streaming:
                    await bot.send_file(
                        e.chat_id,
                        file_name,
                        thumb=thumb,
                        caption=input_str,
                        force_document=False,
                        allow_cache=False,
                        reply_to=e.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=progress,
                    )
                elif round_message:
                    await bot.send_file(
                        e.chat_id,
                        file_name,
                        thumb=thumb,
                        allow_cache=False,
                        reply_to=e.message.id,
                        video_note=True,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=0,
                                w=1,
                                h=1,
                                round_message=True,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=progress,
                    )
                elif spam_big_messages:
                    await e.edit("TBD: Not (yet) Implemented")
                    return
                end = datetime.now()
                ms = (end - start).seconds
                os.remove(thumb)
                await e.edit("Uploaded in {} seconds.".format(ms))
            except FileNotFoundError as e:
                await e.edit(str(e))
        else:
            await e.edit("404: File Not Found")

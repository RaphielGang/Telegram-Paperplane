# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except
# 'download, uploadir, uploadas, upload' which is MPL
# License: MPL and OSSRPL

""" Userbot module which contains everything related to \
    downloading/uploading from/to the server. """

import json
import os
import subprocess
from datetime import datetime

import requests
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from userbot import LOGS, CMD_HELP
from userbot.events import register

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")


def progress(current, total):
    """ Logs the download progress """
    LOGS.info(
        "Downloaded %s of %s\nCompleted %s",
        current, total, (current / total) * 100
    )


@register(pattern=r".download(?: |$)(.*)", outgoing=True)
async def download(target_file):
    """ For .download command, download files to the userbot's server. """
    if not target_file.text[0].isalpha() and target_file.text[0] not in ("/", "#", "@", "!"):
        if target_file.fwd_from:
            return
        await target_file.edit("Processing ...")
        input_str = target_file.pattern_match.group(1)
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        if target_file.reply_to_msg_id:
            start = datetime.now()
            downloaded_file_name = await target_file.client.download_media(
                await target_file.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            end = datetime.now()
            duration = (end - start).seconds
            await target_file.edit(
                "Downloaded to `{}` in {} seconds.".format(
                    downloaded_file_name, duration)
            )
        elif "|" in input_str:
            url, file_name = input_str.split("|")
            url = url.strip()
            # https://stackoverflow.com/a/761825/4723940
            file_name = file_name.strip()
            required_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
            start = datetime.now()
            resp = requests.get(url, stream=True)
            with open(required_file_name, "wb") as file:
                total_length = resp.headers.get("content-length")
                # https://stackoverflow.com/a/15645088/4723940
                if total_length is None:  # no content length header
                    file.write(resp.content)
                else:
                    downloaded = 0
                    total_length = int(total_length)
                    for chunk in resp.iter_content(chunk_size=128):
                        downloaded += len(chunk)
                        file.write(chunk)
                        done = int(100 * downloaded / total_length)
                        download_progress_string = "Downloading ... [%s%s]" % (
                            "=" * done,
                            " " * (50 - done),
                        )
                        LOGS.info(download_progress_string)
            end = datetime.now()
            duration = (end - start).seconds
            await target_file.edit(
                "Downloaded to `{}` in {} seconds.".format(
                    required_file_name, duration)
            )
        else:
            await target_file.edit("Reply to a message to download to my local server.")


@register(pattern=r".uploadir (.*)", outgoing=True)
async def uploadir(udir_event):
    """ For .uploadir command, allows you to upload everything from a folder in the server"""
    if not udir_event.text[0].isalpha() and udir_event.text[0] not in ("/", "#", "@", "!"):
        if udir_event.fwd_from:
            return
        input_str = udir_event.pattern_match.group(1)
        if os.path.exists(input_str):
            start = datetime.now()
            await udir_event.edit("Processing ...")
            lst_of_files = []
            for r, d, f in os.walk(input_str):
                for file in f:
                    lst_of_files.append(os.path.join(r, file))
                for file in d:
                    lst_of_files.append(os.path.join(r, file))
            LOGS.info(lst_of_files)
            uploaded = 0
            await udir_event.edit(
                "Found {} files. Uploading will start soon. Please wait!".format(
                    len(lst_of_files)
                )
            )
            for single_file in lst_of_files:
                if os.path.exists(single_file):
                    # https://stackoverflow.com/a/678242/4723940
                    caption_rts = os.path.basename(single_file)
                    if not caption_rts.lower().endswith(".mp4"):
                        await udir_event.client.send_file(
                            udir_event.chat_id,
                            single_file,
                            caption=caption_rts,
                            force_document=False,
                            allow_cache=False,
                            reply_to=udir_event.message.id,
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
                        await udir_event.client.send_file(
                            udir_event.chat_id,
                            single_file,
                            caption=caption_rts,
                            thumb=thumb_image,
                            force_document=False,
                            allow_cache=False,
                            reply_to=udir_event.message.id,
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
                    uploaded = uploaded + 1
            end = datetime.now()
            duration = (end - start).seconds
            await udir_event.edit("Uploaded {} files in {} seconds.".format(uploaded, duration))
        else:
            await udir_event.edit("404: Directory Not Found")


@register(pattern=r".upload (.*)", outgoing=True)
async def upload(u_event):
    """ For .upload command, allows you to upload a file from the userbot's server """
    if not u_event.text[0].isalpha() and u_event.text[0] not in ("/", "#", "@", "!"):
        if u_event.fwd_from:
            return
        if u_event.is_channel and not u_event.is_group:
            await u_event.edit("`Uploading isn't permitted on channels`")
            return
        await u_event.edit("Processing ...")
        input_str = u_event.pattern_match.group(1)
        if input_str in ("userbot.session", "config.env"):
            await u_event.edit("`That's a dangerous operation! Not Permitted!`")
            return
        if os.path.exists(input_str):
            start = datetime.now()
            await u_event.client.send_file(
                u_event.chat_id,
                input_str,
                force_document=True,
                allow_cache=False,
                reply_to=u_event.message.id,
                progress_callback=progress,
            )
            end = datetime.now()
            duration = (end - start).seconds
            await u_event.edit("Uploaded in {} seconds.".format(duration))
        else:
            await u_event.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    """ Get video thhumbnail """
    metadata = extractMetadata(createParser(file))
    popen = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)
                    [metadata.has("duration")] / 2)
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
    if not popen.returncode and os.path.lexists(file):
        return output
    return None


def extract_w_h(file):
    """ Get width and height of media """
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
        t_response = subprocess.check_output(
            command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@register(pattern=r".uploadas(stream|vn|all) (.*)", outgoing=True)
async def uploadas(uas_event):
    """ For .uploadas command, allows you to specify some arguments for upload. """
    if not uas_event.text[0].isalpha() and uas_event.text[0] not in ("/", "#", "@", "!"):
        if uas_event.fwd_from:
            return
        await uas_event.edit("Processing ...")
        type_of_upload = uas_event.pattern_match.group(1)
        supports_streaming = False
        round_message = False
        spam_big_messages = False
        if type_of_upload == "stream":
            supports_streaming = True
        if type_of_upload == "vn":
            round_message = True
        if type_of_upload == "all":
            spam_big_messages = True
        input_str = uas_event.pattern_match.group(2)
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
                    await uas_event.client.send_file(
                        uas_event.chat_id,
                        file_name,
                        thumb=thumb,
                        caption=input_str,
                        force_document=False,
                        allow_cache=False,
                        reply_to=uas_event.message.id,
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
                    await uas_event.client.send_file(
                        uas_event.chat_id,
                        file_name,
                        thumb=thumb,
                        allow_cache=False,
                        reply_to=uas_event.message.id,
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
                    await uas_event.edit("TBD: Not (yet) Implemented")
                    return
                end = datetime.now()
                duration = (end - start).seconds
                os.remove(thumb)
                await uas_event.edit("Uploaded in {} seconds.".format(duration))
            except FileNotFoundError as err:
                await uas_event.edit(str(err))
        else:
            await uas_event.edit("404: File Not Found")

CMD_HELP.update({
    "download": ".download <link>\nUsage: Downloads file from link to the server."
})
CMD_HELP.update({
    "upload": ".upload <link>\nUsage: Uploads a locally stored file to telegram."
})

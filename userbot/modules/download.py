# Copyright (C) 2019 The Raphielscape Company LLC, Rupansh Sekar.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL
""" Userbot module which contains everything related to
    downloading/uploading from/to the server. """

import json
import logging
import os
import subprocess
from datetime import datetime
from io import BytesIO
from mimetypes import guess_type
from random import randint
from re import findall
from shutil import make_archive

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from psutil import swap_memory, virtual_memory
from pyDownload import Downloader
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from telethon.tl.types import DocumentAttributeVideo, MessageMediaPhoto

from userbot import CMD_HELP, GDRIVE_FOLDER, LOGS
from userbot.events import register

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")


def progress(current, total):
    """ Logs the download progress """
    LOGS.info("Downloaded %s of %s\nCompleted %s", current, total,
              (current / total) * 100)


async def download_from_url(url: str, file_name: str) -> str:
    """
    Download files from URL
    """
    start = datetime.now()
    downloader = Downloader(url=url)
    end = datetime.now()
    duration = (end - start).seconds
    os.rename(downloader.file_name, file_name)
    status = f"Downloaded `{file_name}` in {duration} seconds."
    return status


async def download_from_tg(target_file) -> (str, BytesIO):
    """
    Download files from Telegram
    """
    async def dl_file(buffer: BytesIO) -> BytesIO:
        buffer = await target_file.client.download_media(
            reply_msg,
            buffer,
            progress_callback=progress,
        )
        return buffer

    start = datetime.now()
    buf = BytesIO()
    reply_msg = await target_file.get_reply_message()
    avail_mem = virtual_memory().available + swap_memory().free
    try:
        if reply_msg.media.document.size >= avail_mem:  # unlikely to happen but baalaji crai
            filen = await target_file.client.download_media(
                reply_msg,
                progress_callback=progress,
            )
        else:
            buf = await dl_file(buf)
            filen = reply_msg.media.document.attributes[0].file_name
    except AttributeError:
        buf = await dl_file(buf)
        try:
            filen = reply_msg.media.document.attributes[0].file_name
        except AttributeError:
            if isinstance(reply_msg.media, MessageMediaPhoto):
                filen = 'photo-' + str(datetime.today())\
                    .split('.')[0].replace(' ', '-') + '.jpg'
            else:
                filen = reply_msg.media.document.mime_type\
                    .replace('/', '-' + str(datetime.today())
                             .split('.')[0].replace(' ', '-') + '.')
    end = datetime.now()
    duration = (end - start).seconds
    await target_file.edit(f"`Downloaded {filen} in {duration} seconds.`")
    return filen, buf


async def gdrive_upload(filename: str, filebuf: BytesIO = None) -> str:
    """
    Upload files to Google Drive using PyDrive2
    """
    # a workaround for disabling cache errors
    # https://github.com/googleapis/google-api-python-client/issues/299
    logging.getLogger('googleapiclient.discovery_cache').setLevel(
        logging.CRITICAL)

    # Authenticate Google Drive automatically
    # https://stackoverflow.com/a/24542604
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("secret.json")
    if gauth.credentials is None:
        return "nosecret"
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        # Initialize the saved credentials
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("secret.json")
    drive = GoogleDrive(gauth)

    if filename.count('/') > 1:
        filename = filename.split('/')[-1]
    filedata = {
        'title': filename,
        "parents": [{
            "kind": "drive#fileLink",
            "id": GDRIVE_FOLDER
        }]
    }

    if filebuf:
        mime_type = guess_type(filename)
        if mime_type[0] and mime_type[1]:
            filedata['mimeType'] = f"{mime_type[0]}/{mime_type[1]}"
        else:
            filedata['mimeType'] = 'text/plain'
        file = drive.CreateFile(filedata)
        file.content = filebuf
    else:
        file = drive.CreateFile(filedata)
        file.SetContentFile(filename)
    name = filename.split('/')[-1]
    file.Upload()
    # insert new permission
    file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })
    if not filebuf:
        os.remove(filename)
    reply = f"[{name}]({file['alternateLink']})\n" \
        f"__Direct link:__ [Here]({file['downloadUrl']})"
    return reply


@register(pattern=r"^.mirror(?: |$)([\s\S]*)", outgoing=True)
async def gdrive_mirror(request):
    """ Download a file and upload to Google Drive """
    message = request.pattern_match.group(1)
    if not request.reply_to_msg_id and not message:
        await request.edit("`Usage: .mirror <url> <url>`")
        return
    reply = ''
    reply_msg = await request.get_reply_message()
    links = findall(r'\bhttps?://.*\.\S+', message)
    if not (links or reply_msg or reply_msg.media or reply_msg.media.document):
        reply = "`No links or telegram files found!`\n"
        await request.edit(reply)
        return
    if request.reply_to_msg_id:
        await request.edit('`Downloading from Telegram...`')
        filen, buf = await download_from_tg(request)
        await request.edit(f'`Uploading {filen} to GDrive...`')
        reply += await gdrive_upload(
            filen, buf) if buf else await gdrive_upload(filen)
    elif "|" in message:
        url, file_name = message.split("|")
        url = url.strip()
        file_name = file_name.strip()
        await request.edit(f'`Downloading {file_name}`')
        status = await download_from_url(url, file_name)
        await request.edit(status)
        await request.edit(f'`Uploading {file_name} to GDrive...`')
        reply += await gdrive_upload(file_name)
    if "nosecret" in reply:
        reply = "`Run the generate_drive_session.py file " \
                "in your machine to authenticate on google drive!!`"
    await request.edit(reply)


@register(pattern=r"^.drive(?: |$)(\S*.?\/*.?\.?[A-Za-z0-9]*)", outgoing=True)
async def gdrive(request):
    """ Upload files from server to Google Drive """
    path = request.pattern_match.group(1)
    if not path:
        await request.edit("`Usage: .drive <file>`")
        return
    if not os.path.isfile(path):
        await request.edit("`No such file!`\n")
        return
    file_name = path.split('/')[-1]
    await request.edit(f'`Uploading {file_name} to GDrive...`')
    reply = await gdrive_upload(path)
    await request.edit(reply)


@register(pattern=r"^.download(?: |$)(.*)", outgoing=True)
async def download(file):
    """ Download to local machine"""
    if not file.fwd_from:
        input_str = file.pattern_match.group(1)
        reply_msg = await file.get_reply_message()
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        if reply_msg and reply_msg.media:
            await file.edit('`Downloading file from Telegram....`')
            filen, buf = await download_from_tg(file)
            if buf:
                with open(filen, 'wb') as to_save:
                    to_save.write(buf.read())
        elif "|" in input_str:
            url, file_name = input_str.split("|")
            url = url.strip()
            file_name = file_name.strip()
            await file.edit(f'`Downloading {file_name}`')
            status = await download_from_url(url, file_name)
            await file.edit(status)
        else:
            await file.edit("What am I supposed to download?")


async def upload_f(msg, file_n: str) -> int:
    if os.path.exists(file_n):
        start = datetime.now()
        await msg.client.send_file(
            msg.chat_id,
            file_n,
            force_document=True,
            allow_cache=False,
            reply_to=msg.message.id,
            progress_callback=progress,
        )
        dur = (datetime.now() - start).seconds
        return dur
    else: return 0


@register(pattern=r"^.uploadir (.*)", outgoing=True)
async def uploadir(dirmsg):
    """ upload a dir from local machine"""
    if dirmsg.fwd_from:
        return
    file_n = dirmsg.pattern_match.group(1)
    if os.path.exists(file_n):
        make_archive(file_n+".zip", 'zip', file_n)
        dur = upload_f(dirmsg, file_n)
        await dirmsg.edit(f"`Uploaded {file_n}, {dur} seconds`")
    else:
        await dirmsg.edit("Invalid dir!`")


@register(pattern=r"^.upload (.*)", outgoing=True)
async def upload(umsg):
    """ Upload a file from local machine """
    if umsg.fwd_from:
        return
    if umsg.is_channel and not umsg.is_group:
        await umsg.edit("`Can't upload here!`")
        return
    file_n = umsg.pattern_match.group(1)
    dur = upload_f(umsg, file_n)
    if dur:
        await umsg.edit(f"`File {file_n} uploaded in {dur} seconds`")
    else:
        await umsg.edit("`Invalid file!`")


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
                int((0, metadata.get("duration").seconds
                     )[metadata.has("duration")] / 2)),
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
        t_response = subprocess.check_output(command_to_run,
                                             stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@register(pattern=r"^.uploadas(stream|vn|all) (.*)", outgoing=True)
async def uploadas(umsg):
    """ For .uploadas command, allows you \
    to specify some arguments for upload. """
    if umsg.fwd_from:
        return
    typeu = umsg.pattern_match.group(1)
    stream = typeu == "stream"
    round = typeu == "vn"
    file_n = umsg.pattern_match.group(2)
    if "|" in file_n:
        file_name, thumb = map(lambda x: x.strip(), umsg.split("|"))
    else:
        file_name = file_n
        thumb_path = randint(1, 100) + ".jpg"
        thumb = get_video_thumb(file_name, output=thumb_path)
    if os.path.exists(file_name):
        start = datetime.now()
        metadata = extractMetadata(createParser(file_name))
        dur = metadata.get("duration").seconds if metadata.has("duration") else 0
        w = metadata.get("width") if metadata.has("width") else 1
        h = metadata.get("height") if metadata.has("height") else 1
        try:
            if stream or round:
                await umsg.client.send_file(
                    umsg.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=file_n,
                    force_document=False,
                    allow_cache=False,
                    reply_to=umsg.message.id,
                    video_note=round,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=dur,
                            w=w,
                            h=h,
                            round_message=round,
                            supports_streaming=stream or round,
                        )
                    ],
                    progress_callback=progress,
                )
            end = datetime.now()
            duration = (end - start).seconds
            os.remove(thumb)
            await umsg.edit("Uploaded in {} seconds.".format(duration))
        except FileNotFoundError as err:
            await umsg.edit(str(err))
    else:
        await umsg.edit("Invalid file")

CMD_HELP.update({"download": ['Download',
    " - `.download [in reply to TG file] or .download <link> | <filename>`: "
    "Download a file from telegram or link to the server.\n"
    " - `.upload <link>`: Upload a locally(where Paperplane runs) stored file to Telegram.\n"
    " - `.drive <filename>`: Upload a locally(where Paperplane runs) stored file to GDrive.\n"
    " - `.mirror [in reply to TG file] or .mirror <link> | <filename>`: Mirror a file to Google Drive.\n"]
})

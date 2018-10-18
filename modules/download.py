import json
import os
import subprocess
import requests
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError

from PIL import Image

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")


def progress(current, total):
    print("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@bot.on(events.NewMessage(pattern=r".download (.*)", outgoing=True))
async def _(event):
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
                    # download_progress_string = "Downloading ... [%s of %s]" % (str(dl), str(total_length))
                    # download_progress_string = "Downloading ... [%s%s]" % ('⬛️' * done, '⬜️' * (100 - done))
                    """try:
                        await event.edit(download_progress_string)
                    except MessageNotModifiedError as e:
                        print("__FLOODWAIT__: {} sleeping for 100seconds, before proceeding.".format(str(e)))
                    time.sleep(1)"""
                    print(download_progress_string)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(required_file_name, ms))
    else:
        await event.edit("Reply to a message to download to my local server.")

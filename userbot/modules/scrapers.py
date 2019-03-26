# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

import os
import re
from asyncio import create_subprocess_shell as asyncsh
from asyncio.subprocess import PIPE as asyncsh_PIPE
import requests

import urbandict
import wikipedia
from google_images_download import google_images_download
from googletrans import Translator
from gtts import gTTS
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
from pytube.helpers import safe_filename

from userbot import LOGGER, LOGGER_GROUP, YOUTUBE_API_KEY, HELPER, bot
from userbot.events import register

langi = "en"


@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Processing...")
        s = e.pattern_match.group(1)
        lim = re.findall(r"lim=\d+", s)
        try:
            lim = lim[0]
            lim = lim.replace("lim=", "")
            s = s.replace("lim=" + lim[0], "")
        except IndexError:
            lim = 2
        response = google_images_download.googleimagesdownload()

        # creating list of arguments
        arguments = {
            "keywords": s,
            "limit": lim,
            "format": "jpg",
        }

        # passing the arguments to the function
        paths = response.download(arguments)
        lst = paths[s]
        await e.client.send_file(await e.client.get_input_entity(e.chat_id), lst)
        await e.delete()


@register(outgoing=True, pattern=r"^.google (.*)")
async def gsearch(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        match = e.pattern_match.group(1)
        result_ = await asyncsh(
            f"gsearch {match}",
            stdout=asyncsh_PIPE,
            stderr=asyncsh_PIPE
            )
        stdout, stderr = await result_.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())
        await e.edit(
            "**Search Query:**\n`" + match + "`\n\n**Result:**\n" + result
        )
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "Google Search query " + match + " was executed successfully",
            )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        match = e.pattern_match.group(1)
        result = wikipedia.summary(match)
        await e.edit(
            "**Search:**\n`" + match + "`\n\n**Result:**\n" + result
        )
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                f"Wiki query {match} was executed successfully"
            )


@register(outgoing=True, pattern="^.ud (.*)")
async def ud(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Processing...")
        str = e.pattern_match.group(1)
        mean = urbandict.define(str)
        if len(mean) >= 0:
            await e.edit(
                "Text: **"
                + str
                + "**\n\nMeaning: **"
                + mean[0]["def"]
                + "**\n\n"
                + "Example: \n__"
                + mean[0]["example"]
                + "__"
            )
            if LOGGER:
                await e.client.send_message(
                    LOGGER_GROUP, "ud query " + str + " executed successfully."
                )
        else:
            await e.edit("No result found for **" + str + "**")


@register(outgoing=True, pattern="^.tts")
async def tts(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        replye = e.text
        if replye[5:]:
            message = str(replye[5:])
        elif textx:
            message = textx
            message = str(message.message)
        tts = gTTS(message, langi)
        tts.save("k.mp3")
        with open("k.mp3", "rb") as f:
            linelist = list(f)
            linecount = len(linelist)
        if linecount == 1:
            try:  # tts on personal chats is broken
                tts = gTTS(message, langi)
                tts.save("k.mp3")
            except:
                await e.edit("`Some Internal Error! Try Again!`")
                return
        with open("k.mp3", "r"):
            await e.client.send_file(e.chat_id, "k.mp3", voice_note=True)
            os.remove("k.mp3")
            if LOGGER:
                await e.client.send_message(
                    LOGGER_GROUP, "tts of " + message + " executed successfully!"
                )
            await e.delete()


@register(outgoing=True, pattern="^.trt")
async def translateme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global langi
        translator = Translator()
        textx = await e.get_reply_message()
        message = e.text
        if message[4:]:
            message = str(message[4:])
        elif textx:
            message = textx
            message = str(message.message)

        reply_text = translator.translate(message, dest=langi).text
        reply_text = f"**Source:** `\n {message} `**\n\nTranslation: **`\n {reply_text} `"

        await e.client.send_message(e.chat_id, reply_text)
        await e.delete()
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                f"Translate query {message} was executed successfully",
            )


@register(pattern=".lang", outgoing=True)
async def lang(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global langi
        message = await e.client.get_messages(e.chat_id)
        langi = str(message[0].message[6:])
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP, "tts language changed to **" + langi + "**"
            )
            await e.edit("tts language changed to **" + langi + "**")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    if not video_q.text[0].isalpha() and video_q.text[0] not in ("/", "#", "@", "!"):
        query = video_q.pattern_match.group(1)
        result = ''
        i = 1
        full_response = youtube_search(query)
        videos_json = full_response[1]

        await video_q.edit("```Processing...```")
        for video in videos_json:
            print(video['snippet']['title'])
            result += f"{i}. {video['snippet']['title']} \n   https://www.youtube.com/watch?v={video['id']['videoId']} \n"
            i += 1

        reply_text = f"**Search Query:**\n` {query} `\n\n**Result:**\n {result}"

        await video_q.edit(reply_text)


def youtube_search(q, max_results=10, order="relevance", token=None, location=None, location_radius=None):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=max_results,
        location=location,
        locationRadius=location_radius
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return(nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return(nexttok, videos)


@register(outgoing=True, pattern=".yt_dl (\S*)( (\S*))?")
async def download_video(v_url):
    if not v_url.text[0].isalpha() and v_url.text[0] not in ("/", "#", "@", "!"):
        url = v_url.pattern_match.group(1)
        quality = v_url.pattern_match.group(3)

        await v_url.edit("**Fetching...**")

        video = YouTube(url)

        if quality:
            video_stream = video.streams.filter(
                progressive=True,
                subtype="mp4",
                res=quality
            ).first()
        else:
            video_stream = video.streams.filter(
                progressive=True,
                subtype="mp4"
            ).first()

        if video_stream is None:
            all_streams = video.streams.filter(
                progressive=True,
                subtype="mp4"
            ).all()
            available_qualities = ""

            for item in all_streams[:-1]:
                available_qualities += f"{item.resolution}, "
            available_qualities += all_streams[-1].resolution

            await v_url.edit(
                "**A stream matching your query wasn't found. Try again with different options.\n**"
                "**Available Qualities:**\n"
                f"{available_qualities}"
            )
            return

        video_size = video_stream.filesize / 1000000

        if video_size >= 50:
            await v_url.edit(
                ("**File larger than 50MB. Sending the link instead.\n**"
                 f"Get the video [here]({video_stream.url})\n\n"
                 "**If the video opens instead of playing, right-click(or long press) and "
                 "press 'Save Video As...'(may depend on the browser) to download the video.**")
            )
            return

        await v_url.edit("**Downloading...**")

        video_stream.download(filename=video.title)

        url = video.thumbnail_url
        r = requests.get(url)
        with open('thumbnail.jpg', 'wb') as fs:
            fs.write(r.content)

        await v_url.edit("**Uploading...**")
        await bot.send_file(
            v_url.chat_id,
            f'{safe_filename(video.title)}.mp4',
            caption=f"{video.title}",
            thumb="thumbnail.jpg"
        )

        os.remove(f"{safe_filename(video.title)}.mp4")
        os.remove('thumbnail.jpg')
        await v_url.delete()

HELPER.update({
    'yt_dl <url> <quality>(optional)': "Usage: \nDownload videos from YouTube. If no quality is specified, the highest downloadable quality is downloaded. Will send the link if the video is larger than 50 MB."
})

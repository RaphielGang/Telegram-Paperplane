# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module containing various scrapers. """

import html
import os
import re
import urllib
from asyncio import create_subprocess_shell as asyncsh
from asyncio.subprocess import PIPE as asyncsh_PIPE

import requests
import urbandict
import wikipedia
from google_images_download import google_images_download
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from pytube import YouTube
from pytube.helpers import safe_filename

from userbot import HELPER, LOGGER, LOGGER_GROUP, YOUTUBE_API_KEY, bot
from userbot.events import register

LANG = "en"


@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("Processing...")
        query = event.pattern_match.group(1)
        lim = re.findall(r"lim=\d+", query)
        try:
            lim = lim[0]
            lim = lim.replace("lim=", "")
            query = query.replace("lim=" + lim[0], "")
        except IndexError:
            lim = 2
        response = google_images_download.googleimagesdownload()

        # creating list of arguments
        arguments = {
            "keywords": query,
            "limit": lim,
            "format": "jpg",
            "no_directory": "no_directory"
        }

        # passing the arguments to the function
        paths = response.download(arguments)
        lst = paths[query]
        await event.client.send_file(await event.client.get_input_entity(event.chat_id), lst)
        os.remove(lst[0])
        os.remove(lst[1])
        os.rmdir(os.path.dirname(os.path.abspath(lst[0])))
        await event.delete()


@register(outgoing=True, pattern=r"^.google (.*)")
async def gsearch(q_event):
    """ For .google command, do a Google search. """
    if not q_event.text[0].isalpha() and q_event.text[0] not in ("/", "#", "@", "!"):
        match_ = q_event.pattern_match.group(1)
        match = urllib.parse.quote_plus(match_)
        result_ = await asyncsh(
            f"gsearch {match}",
            stdout=asyncsh_PIPE,
            stderr=asyncsh_PIPE
            )
        stdout, stderr = await result_.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())
        await q_event.edit(
            "**Search Query:**\n`" + match_ + "`\n\n**Result:**\n" + result
        )
        if LOGGER:
            await q_event.client.send_message(
                LOGGER_GROUP,
                "Google Search query " + match_ + " was executed successfully",
            )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ For .google command, fetch content from Wikipedia. """
    if not wiki_q.text[0].isalpha() and wiki_q.text[0] not in ("/", "#", "@", "!"):
        match = wiki_q.pattern_match.group(1)
        try:
            wikipedia.summary(match)
        except wikipedia.exceptions.DisambiguationError as error:
            await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
            return
        except wikipedia.exceptions.PageError as pageerror:
            await wiki_q.edit(f"Page not found.\n\n{pageerror}")
            return
        result = wikipedia.summary(match)
        if len(result) >= 4096:
            file = open("output.txt", "w+")
            file.write(result)
            file.close()
            await wiki_q.client.send_file(
                wiki_q.chat_id,
                "output.txt",
                reply_to=wiki_q.id,
                caption="`Output too large, sending as file`",
            )
            if os.path.exists("output.txt"):
                os.remove("output.txt")
            return
        await wiki_q.edit(
            "**Search:**\n`" + match + "`\n\n**Result:**\n" + result
        )
        if LOGGER:
            await wiki_q.client.send_message(
                LOGGER_GROUP,
                f"Wiki query {match} was executed successfully"
            )


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ For .ud command, fetch content from Urban Dictionary. """
    if not ud_e.text[0].isalpha() and ud_e.text[0] not in ("/", "#", "@", "!"):
        await ud_e.edit("Processing...")
        query = ud_e.pattern_match.group(1)
        try:
            urbandict.define(query)
        except urllib.error.HTTPError:
            await ud_e.edit(f"Sorry, couldn't find any results for: {query}")
            return
        mean = urbandict.define(query)
        deflen = sum(len(i) for i in mean[0]["def"])
        exalen = sum(len(i) for i in mean[0]["example"])
        meanlen = deflen + exalen
        if int(meanlen) >= 0:
            if int(meanlen) >= 4096:
                await ud_e.edit("`Output too large, sending as file.`")
                file = open("output.txt", "w+")
                file.write(
                    "Text: "
                    + query
                    + "\n\nMeaning: "
                    + mean[0]["def"]
                    + "\n\n"
                    + "Example: \n"
                    + mean[0]["example"]
                )
                file.close()
                await ud_e.client.send_file(
                    ud_e.chat_id,
                    "output.txt",
                    caption="`Output was too large, sent it as a file.`"
                )
                if os.path.exists("output.txt"):
                    os.remove("output.txt")
                await ud_e.delete()
                return
            await ud_e.edit(
                "Text: **"
                + query
                + "**\n\nMeaning: **"
                + mean[0]["def"]
                + "**\n\n"
                + "Example: \n__"
                + mean[0]["example"]
                + "__"
            )
            if LOGGER:
                await ud_e.client.send_message(
                    LOGGER_GROUP, "ud query " + query + " executed successfully."
                )
        else:
            await ud_e.edit("No result found for **" + query + "**")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ For .tts command, a wrapper for Google Text-to-Speech. """
    if not query.text[0].isalpha() and query.text[0] not in ("/", "#", "@", "!"):
        textx = await query.get_reply_message()
        message = query.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await query.edit("`Give a text or reply to a message for Text-to-Speech!`")
            return

        try:
            gTTS(message, LANG)
        except AssertionError:
            await query.edit(
                'The text is empty.\n'
                'Nothing left to speak after pre-precessing, tokenizing and cleaning.'
            )
            return
        except ValueError:
            await query.edit('Language is not supported.')
            return
        except RuntimeError:
            await query.edit('Error loading the languages dictionary.')
            return
        tts = gTTS(message, LANG)
        tts.save("k.mp3")
        with open("k.mp3", "rb") as audio:
            linelist = list(audio)
            linecount = len(linelist)
        if linecount == 1:
            tts = gTTS(message, LANG)
            tts.save("k.mp3")
        with open("k.mp3", "r"):
            await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
            os.remove("k.mp3")
            if LOGGER:
                await query.client.send_message(
                    LOGGER_GROUP, "tts of " + message + " executed successfully!"
                )
            await query.delete()


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)") # ^.promote(?: |$)(.*)
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    if not trans.text[0].isalpha() and trans.text[0] not in ("/", "#", "@", "!"):
        translator = Translator()
        textx = await trans.get_reply_message()
        message = trans.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await trans.edit("`Give a text or reply to a message to translate!`")
            return

        try:
            reply_text = translator.translate(deEmojify(message), dest=LANG)
        except ValueError:
            await trans.edit("Invalid destination language.")
            return

        source_lan = LANGUAGES[f'{reply_text.src}']
        transl_lan = LANGUAGES[f'{reply_text.dest}']
        reply_text = f"**Source ({source_lan.title()}):**`\n{message}`**\n\
\nTranslation ({transl_lan.title()}):**`\n{reply_text.text}`"

        await trans.client.send_message(trans.chat_id, reply_text)
        await trans.delete()
        if LOGGER:
            await trans.client.send_message(
                LOGGER_GROUP,
                f"Translate query {message} was executed successfully",
            )


@register(pattern=".lang (.*)", outgoing=True)
async def lang(value):
    """ For .lang command, change the default langauge of userbot scrapers. """
    if not value.text[0].isalpha() and value.text[0] not in ("/", "#", "@", "!"):
        global LANG
        LANG = value.pattern_match.group(1)
        if LOGGER:
            await value.client.send_message(
                LOGGER_GROUP, "Default language changed to **" + LANG + "**"
            )
            await value.edit("Default language changed to **" + LANG + "**")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ For .yt command, do a YouTube search from Telegram. """
    if not video_q.text[0].isalpha() and video_q.text[0] not in ("/", "#", "@", "!"):
        query = video_q.pattern_match.group(1)
        result = ''
        i = 1
        full_response = youtube_search(query)
        videos_json = full_response[1]

        await video_q.edit("```Processing...```")
        for video in videos_json:
            result += f"{i}. {html.unescape(video['snippet']['title'])} \
                \nhttps://www.youtube.com/watch?v={video['id']['videoId']}\n"
            i += 1

        reply_text = f"**Search Query:**\n`{query}`\n\n**Result:**\n{result}"

        await video_q.edit(reply_text)


def youtube_search(
        query,
        order="relevance",
        token=None,
        location=None,
        location_radius=None
    ):
    """ Do a YouTube search. """
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=10,
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
    except KeyError:
        nexttok = "KeyError, try again."
        return(nexttok, videos)


@register(outgoing=True, pattern=r".yt_dl (\S*) ?(\S*)")
async def download_video(v_url):
    """ For .yt_dl command, download videos from YouTube. """
    if not v_url.text[0].isalpha() and v_url.text[0] not in ("/", "#", "@", "!"):
        url = v_url.pattern_match.group(1)
        quality = v_url.pattern_match.group(2)

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
        resp = requests.get(url)
        with open('thumbnail.jpg', 'wb') as file:
            file.write(resp.content)

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

def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return inputString.encode('ascii', 'ignore').decode('ascii')

HELPER.update({
    'img': ".img <search_query>\
    \nUsage: Does an image search on Google and shows two images."
})
HELPER.update({
    'google': ".google <search_query>\
    \nUsage: Does a search on Google."
})
HELPER.update({
    'wiki': ".wiki <search_query>\
    \nUsage: Does a Wikipedia search."
})
HELPER.update({
    'ud': ".ud <search_query>\
    \nUsage: Does a search on Urban Dictionary."
})
HELPER.update({
    'tts': ".tts <text> or reply to someones text with .trt\
    \nUsage: Translates text to speech for the default language which is set."
})
HELPER.update({
    'trt': ".trt <text> or reply to someones text with .trt\
    \nUsage: Translates text to the default language which is set."
})
HELPER.update({
    'lang': ".lang <lang>\
    \nUsage: Changes the default language of userbot scrapers used for Google TRT, \
    TTS may not work."
})
HELPER.update({
    'yt': ".yt <search_query>\
    \nUsage: Does a YouTube search. "
})
HELPER.update({
    'yt_dl': ".yt_dl <url> <quality>(optional)\
    \nUsage: Download videos from YouTube. \
If no quality is specified, the highest downloadable quality is downloaded. \
Will send the link if the video is larger than 50 MB."
})

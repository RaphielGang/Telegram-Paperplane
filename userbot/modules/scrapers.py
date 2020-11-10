# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various scrapers. """

import io
import asyncio
import os
import time
import urllib
import requests
import re

from PIL import Image
from bs4 import BeautifulSoup
from re import findall
from shutil import rmtree
from urllib.error import HTTPError
from emoji import get_emoji_regexp
from googletrans import LANGUAGES, Translator
from gtts import gTTS, gTTSError
from search_engine_parser import GoogleSearch
from urbandict import define
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)

from telethon.tl.types import DocumentAttributeAudio

from userbot.utils.google_images_download import googleimagesdownload
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.modules.upload_download import progress

opener = urllib.request.build_opener()
useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/80.0.3987.149 Mobile Safari/537.36'
             )
opener.addheaders = [('User-agent', useragent)]

# Default language to EN
LANG = "en"


@register(outgoing=True, pattern="^\.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("Processing...")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 2
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory"
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst)
    rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


@register(outgoing=True, pattern=r"^\.google(?: |$)(.*)")
async def gsearch(q_event):
    """ For .google command, do a Google search. """
    textx = await q_event.get_reply_message()
    query = q_event.pattern_match.group(1)

    if query:
        pass
    elif textx:
        query = textx.text
    else:
        await q_event.edit("`Pass a query as an argument or reply "
                           "to a message for Google search!`")
        return

    await q_event.edit("`Searching...`")

    search_args = (str(query), 1)
    googsearch = GoogleSearch()
    gresults = await googsearch.async_search(*search_args)
    msg = ""
    for i in range(1, 6):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"{i}. [{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Search Query:**\n`" + query + "`\n\n**Results:**\n" +
                       msg,
                       link_preview=False)
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + query + "` was executed successfully",
        )


@register(outgoing=True, pattern=r"^\.wiki (.*)")
async def wiki(wiki_q):
    """ For .google command, fetch content from Wikipedia. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Page not found.\n\n{pageerror}")
        return
    result = summary(match)
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
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query {match} was executed successfully")


@register(outgoing=True, pattern="^\.ud (.*)")
async def urban_dict(ud_e):
    """ For .ud command, fetch content from Urban Dictionary. """
    await ud_e.edit("Processing...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Sorry, couldn't find any results for: {query}")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Output too large, sending as file.`")
            file = open("output.txt", "w+")
            file.write("Text: " + query + "\n\nMeaning: " + mean[0]["def"] +
                       "\n\n" + "Example: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "output.txt",
                caption="`Output was too large, sent it as a file.`")
            if os.path.exists("output.txt"):
                os.remove("output.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Text: **" + query + "**\n\nMeaning: **" +
                        mean[0]["def"] + "**\n\n" + "Example: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID, "ud query " + query + " executed successfully.")
    else:
        await ud_e.edit("No result found for **" + query + "**")


@register(outgoing=True, pattern=r"^\.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ For .tts command, a wrapper for Google Text-to-Speech. """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit("`Give a text or reply to a "
                         "message for Text-to-Speech!`")
        return

    try:
        tts = gTTS(message, tld='com', lang=LANG)
        tts.save("k.mp3")
    except AssertionError:
        await query.edit('The text is empty.\n'
                         'Nothing left to speak after pre-precessing, '
                         'tokenizing and cleaning.')
        return
    except ValueError:
        await query.edit('Language is not supported.')
        return
    except RuntimeError:
        await query.edit('Error loading the languages dictionary.')
        return
    except gTTSError:
        await query.edit('Error in Google Text-to-Speech API request! '
                         'Check Paperplane logs for details.')
        return

    with open("k.mp3", "r"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
        os.remove("k.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "TTS of " + message + " executed successfully!")
        await query.delete()


@register(outgoing=True, pattern=r"^\.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Give a text or reply "
                         "to a message to translate!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=LANG)
    except ValueError:
        await trans.edit("Invalid destination language.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"**Source ({source_lan.title()}):**`\n{message}`**\n\
\nTranslation ({transl_lan.title()}):**`\n{reply_text.text}`"

    await trans.client.send_message(trans.chat_id, reply_text)
    await trans.delete()
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Translate query {message} was executed successfully",
        )


@register(pattern="^\.lang (.*)", outgoing=True)
async def lang(value):
    """ For .lang command, change the default langauge of userbot scrapers. """
    global LANG
    LANG = value.pattern_match.group(1)
    await value.edit("Default language changed to **" + LANG + "**")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, "Default language changed to **" + LANG + "**")


@register(outgoing=True, pattern=r"^\.rip(audio|video) (.*)")
async def download_video(v_url):
    """ For .rip command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Preparing to download...`")

    if type == "audio":
        opts = {
            'format':
                'bestaudio',
            'addmetadata':
                True,
            'key':
                'FFmpegMetadata',
            'writethumbnail':
                True,
            'prefer_ffmpeg':
                True,
            'geo_bypass':
                True,
            'nocheckcertificate':
                True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
                '%(id)s.mp3',
            'quiet':
                True,
            'logtostderr':
                False
        }
        video = False
        song = True

    elif type == "video":
        opts = {
            'format':
                'best',
            'addmetadata':
                True,
            'key':
                'FFmpegMetadata',
            'prefer_ffmpeg':
                True,
            'geo_bypass':
                True,
            'nocheckcertificate':
                True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
                '%(id)s.mp4',
            'logtostderr':
                False,
            'quiet':
                True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await v_url.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Preparing to upload song:`\
        \n**{rip_data['title']}**\
        \nby __{rip_data['uploader']}__")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Preparing to upload video:`\
        \n**{rip_data['title']}**\
        \nby __{rip_data['uploader']}__")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()


@register(outgoing=True, pattern=r"^\.reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, Google search images and stickers. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await bot.download_media(message, photo)
    else:
        return await img.edit("`Reply to photo or sticker nigger.`")

    if photo:
        await img.edit("`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            return await img.edit('`Unsupported sexuality, most likely.`')
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {
            'encoded_image': (name, open(name, 'rb')),
            'image_content': ''
        }
        response = requests.post(searchUrl,
                                 files=multipart,
                                 allow_redirects=False)
        fetchUrl = response.headers['Location']

        if response != 400:
            await img.edit("`Image successfully uploaded to Google. Maybe.`"
                           "\n`Parsing source now. Maybe.`")
        else:
            return await img.edit("`Google told me to fuck off.`")

        os.remove(name)
        match = await ParseSauce(fetchUrl +
                                 "&preferences?hl=en&fg=1#languages")
        guess = match['best_guess']
        imgspage = match['similar_images']

        if guess and imgspage:
            await img.edit(f"[{guess}]({fetchUrl})\n\n`Looking for images...`")
        else:
            return await img.edit("`Couldn't find anything for your uglyass.`")

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(entity=await
                                       img.client.get_input_entity(img.chat_id
                                                                   ),
                                       file=yeet,
                                       reply_to=img)
        except TypeError:
            pass
        await img.edit(
            f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})")


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')

    results = {'similar_images': '', 'best_guess': ''}

    try:
        for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
            url = 'https://www.google.com/search?tbm=isch&q=' + \
                urllib.parse.quote_plus(similar_image.get('value'))
            results['similar_images'] = url
    except BaseException:
        pass

    for best_guess in soup.findAll('div', attrs={'class': 'r5a77d'}):
        results['best_guess'] = best_guess.get_text()

    return results


async def scam(results, lim):

    single = opener.open(results['similar_images']).read()
    decoded = single.decode('utf-8')

    imglinks = []
    counter = 0

    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        if counter < int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks


def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update(
    {
        "scrapers": [
            'Scrapers', " - `img` <query> lim=<n>: Do an Image Search on Google and send n results. Default is 2.\n"
            " - `google` <query>: Search Google for query (argument or reply).\n"
            " - `wiki` <query>: Search Wikipedia for query.\n"
            " - `ud` <query>: Search on Urban Dictionary for query.\n"
            " - `tts` <query>: Text-to-Speech the query (argument or reply) to the saved language.\n"
            " - `trt` <query>: Translate the query (argument or reply) to the saved language.\n"
            " - `lang` <lang>: Changes the default language of trt and TTS modules.\n"
            " - `ripaudio` <url> or `ripvideo` <url>: Download videos and songs from YouTube (and [many other sites](https://ytdl-org.github.io/youtube-dl/supportedsites.html)).\n"
            " - `reverse`: Reply to a pic/sticker to revers-search it on Google Images\n\n"
            "**All commands can be used with** `.`"]})

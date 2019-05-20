# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for reverse image search from google. """

import io
import os
import urllib
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
from telethon.tl.types import MessageMediaPhoto
from PIL import Image

from userbot import bot, HELPER
from userbot.events import register


opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]


@register(outgoing=True, pattern=r"^.reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, reverse image search on google"""
    if not img.text[0].isalpha() and img.text[0] not in ("/", "#", "@", "!"):

        if os.path.isfile("okgoogle.png"):
            os.remove("okgoogle.png")

        message = await img.get_reply_message()
        if message and message.media:
            photo = io.BytesIO()
            await bot.download_media(message, photo)
        else:
            await img.edit("`Reply to photo or sticker nibba.`")
            return

        if photo:
            await img.edit("`Processing...`")
            try:
                image = Image.open(photo)
            except OSError:
                await img.edit('`Gifs And Videos aren't supported yet:/ `')
                return
            name = "okgoogle.png"
            image.save(name, "PNG")
            image.close()
            #https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
            searchUrl = 'https://www.google.com/searchbyimage/upload'
            multipart = {'encoded_image': (name, open(name, 'rb')), 'image_content': ''}
            response = requests.post(searchUrl, files=multipart, allow_redirects=False)
            fetchUrl = response.headers['Location']

            if response != 400:
                await img.edit("`Image successfully uploaded to Google. Maybe.`"
                               "\n`Parsing source now. Maybe.`")
            else:
                await img.edit("`Google told me to fuck off.`")
                return

            os.remove(name)
            match = ParseSauce(fetchUrl + "&hl=en")
            guess = match['best_guess']
            imgspage = match['similar_images']

            if guess and imgspage:
                await img.edit(f"[{guess}]({fetchUrl})\n\n`Looking for images...`")
            else:
                await img.edit("`Couldn't find anything for your search.`")
                return

            if img.pattern_match.group(1):
                lim = img.pattern_match.group(1)
            else:
                lim = 3
            images = scam(match, lim)
            yeet = []
            for i in images:
                k = requests.get(i)
                yeet.append(k.content)
            try:
                await img.client.send_file(entity=await img.client.get_input_entity(img.chat_id),
                                            file=yeet,
                                            reply_to=img)
            except TypeError:
                pass
            await img.edit(f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})")


def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, 'html.parser')

    results = {
        'similar_images': '',
        'best_guess': ''
    }

    try:
        for similar_image in soup.findAll('input', {'class': 'gLFyf'}):
            url = 'https://www.google.com/search?tbm=isch&q=' + urllib.parse.quote_plus(similar_image.get('value'))
            results['similar_images'] = url
    except:
        pass

    for best_guess in soup.findAll('div', attrs={'class':'r5a77d'}):
        results['best_guess'] = best_guess.get_text()

    return results

def scam(results, lim):

    single = opener.open(results['similar_images']).read()
    decoded = single.decode('utf-8')

    imglinks = []
    counter = 0

    pattern = r'^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$'
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        imglinks.append(imglink)
        if counter >= int(lim):
            break

    return imglinks

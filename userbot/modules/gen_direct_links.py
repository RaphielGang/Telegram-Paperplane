# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various sites direct links generators"""

import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

DRIVE = 'https://drive.google.com'


@register(outgoing=True, pattern=r"^.gdrive(?: |$)([\s\S]*)")
async def gdrive(request):
    """ GDrive direct links generator """
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        message = request.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await request.edit("`Usage: .gdrive url`")
            return
        reply = ''
        links = re.findall(r'\bhttps?://drive\.google\.com\S+', message)
        if not links:
            reply = "No Google drive links found"
            await request.edit(reply)
        for link in links:
            file_id = ''
            if link.find("view") != -1:
                file_id = link.split('/')[-2]
            elif link.find("open?id=") != -1:
                file_id = link.split("open?id=")[1].strip()
            elif link.find("uc?id=") != -1:
                file_id = link.split("uc?id=")[1].strip()
            url = f'{DRIVE}/uc?export=download&id={file_id}'
            download = requests.get(url, stream=True, allow_redirects=False)
            cookies = download.cookies
            try:
                # In case of small file size, Google downloads directly
                dl_url = download.headers["location"]
                if 'accounts.google.com' in dl_url:  # non-public file
                    reply += 'Link is not public!'
                    continue
                name = 'Direct Download Link'
            except KeyError:
                # In case of download warning page
                page = BeautifulSoup(download.content, 'html.parser')
                export = DRIVE + page.find('a', {'id': 'uc-download-link'}).get('href')
                name = page.find('span', {'class': 'uc-name-size'}).text
                response = requests.get(export, stream=True, allow_redirects=False, cookies=cookies)
                dl_url = response.headers['location']
                if 'accounts.google.com' in dl_url:
                    reply += 'Link is not public!'
                    continue
            reply += f'[{name}]({dl_url})\n'
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.zippy(?: |$)([\s\S]*)")
async def zippy_share(request):
    """ ZippyShare direct links generator
    Based on https://github.com/LameLemon/ziggy"""
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        message = request.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await request.edit("`Usage: .zippy url`")
            return
        reply = ''
        dl_url = ''
        links = re.findall(r'\bhttps?://.*zippyshare\.com\S+', message)
        if not links:
            reply = "No ZippyShare links found"
            await request.edit(reply)
        for link in links:
            session = requests.Session()
            base_url = re.search('http.+.com', link).group()
            response = session.get(link)
            page_soup = BeautifulSoup(response.content, "lxml")
            scripts = page_soup.find_all("script", {"type": "text/javascript"})
            for script in scripts:
                if "getElementById('dlbutton')" in script.text:
                    url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);', script.text).group('url')
                    math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);', script.text).group('math')
                    dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
                    break
            dl_url = base_url + eval(dl_url)
            name = urllib.parse.unquote(dl_url.split('/')[-1])
            reply += f'[{name}]({dl_url})\n'
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.yadisk(?: |$)([\s\S]*)")
async def yandex_disk(request):
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        message = request.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await request.edit("`Usage: .yadisk url`")
            return
        reply = ''
        links = re.findall(r'\bhttps?://.*yadi\.sk\S+', message)
        if not links:
            reply = "No Yandex.Disk links found"
            await request.edit(reply)
        for link in links:
            api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
            try:
                dl_url = requests.get(api.format(link)).json()['href']
                name = dl_url.split('filename=')[1].split('&disposition')[0]
                reply += f'[{name}]({dl_url})\n'
            except KeyError:
                reply += 'Error: File not found / Download limit reached'
                continue
        await request.edit(reply)


CMD_HELP.update({
    "gdrive": ".gdrive <url> <url>\nUsage: Generate direct download link from Google Drive URL(s)"
})
CMD_HELP.update({
    "yadisk": ".yadisk <url> <url>\nUsage: Generate direct download link from Yandex.Disk URL(s)"
})
CMD_HELP.update({
    "zippy": ".gdrive <url> <url>\nUsage: Generate direct download link from ZippyShare URL(s)"
})

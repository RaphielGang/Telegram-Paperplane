# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various sites direct links generators"""

import re
from requests import get
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
            reply = "No Google drive link found"
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
            download = get(url, stream=True, allow_redirects=False)
            cookies = download.cookies
            try:
                # In case of small file size, Google downloads directly
                direct = download.headers["location"]
                if 'accounts.google.com' in direct:  # non-public file
                    reply += 'Link is not public!'
                    continue
                name = 'Direct Download Link'
            except KeyError:
                # In case of download warning page
                page = BeautifulSoup(download.content, 'html.parser')
                export = DRIVE + page.find('a', {'id': 'uc-download-link'}).get('href')
                name = page.find('span', {'class': 'uc-name-size'}).text
                response = get(export, stream=True, allow_redirects=False, cookies=cookies)
                direct = response.headers['location']
                if 'accounts.google.com' in direct:
                    reply += 'Link is not public!'
                    continue
            reply += f'[{name}]({direct})\n'
        await request.edit(reply)


CMD_HELP.update({
    "gdrive": ".gdrive <url> <url>\nUsage: Generate direct download link from Google Drive URL(s)"
})

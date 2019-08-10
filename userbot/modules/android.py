# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import re
from requests import get
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.events import register, errors_handler


DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@register(outgoing=True, pattern="^.magisk$")
@errors_handler
async def magisk(request):
    """ magisk latest releases """
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        MAGISK_STABLE = get("https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json").json()
        MAGISK_BETA = get("https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json").json()
        MAGISK_CANARY = get("https://raw.githubusercontent.com/topjohnwu/magisk_files/master/canary_builds/canary.json").json()
        stable_releases = 'Latest Stable Magisk Release:\n'
        beta_releases = 'Latest Beta Magisk Release:\n'
        canary_releases = 'Latest Canary Magisk Release:\n'
        try:
            stable_releases += f'APK: [{MAGISK_STABLE["app"]["version"]}]({MAGISK_STABLE["app"]["link"]}) - '
        except NameError:
            stable_releases += f"`can't find latest stable apk`\n"
        try:
            stable_releases += f'ZIP: [{MAGISK_STABLE["magisk"]["version"]}]({MAGISK_STABLE["magisk"]["link"]}) - '
        except NameError:
            stable_releases += f"`can't find latest stable zip`\n"
        try:
            stable_releases += f'[Stable Uninstaller]({MAGISK_STABLE["uninstaller"]["link"]})\n'
        except NameError:
            stable_releases += f"`can't find latest stable uninstaller`\n"
        try:
            beta_releases += f'APK: [{MAGISK_BETA["app"]["version"]}]({MAGISK_BETA["app"]["link"]}) - '
        except NameError:
            beta_releases += f"`can't find latest beta apk`\n"
        try:
            beta_releases += f'ZIP: [{MAGISK_BETA["magisk"]["version"]}]({MAGISK_BETA["magisk"]["link"]}) - '
        except NameError:
            beta_releases += f"`can't find latest beta zip`\n"
        try:
            beta_releases += f'[Beta Uninstaller]({MAGISK_BETA["uninstaller"]["link"]})\n'
        except NameError:
            beta_releases += f"`can't find latest beta uninstaller`\n"
        try:
            canary_releases += f'APK: [{MAGISK_CANARY["app"]["version"]}]({MAGISK_CANARY["app"]["link"]}) - '
        except NameError:
            canary_releases += f"`can't find latest canary apk`\n"
        try:
            canary_releases += f'ZIP: [{MAGISK_CANARY["magisk"]["version"]}]({MAGISK_CANARY["magisk"]["link"]}) - '
        except NameError:
            canary_releases += f"`can't find latest canary zip`\n"
        try:
            canary_releases += f'[Canary Uninstaller]({MAGISK_CANARY["uninstaller"]["link"]})'
        except NameError:
            canary_releases += f"`can't find latest canary uninstaller`"
        await request.edit(f"{stable_releases}{beta_releases}{canary_releases}")


@register(outgoing=True, pattern=r"^.device(?: |$)(\S*)")
@errors_handler
async def device_info(request):
    """ get android device basic info from its codename """
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        device = request.pattern_match.group(1)
        if device:
            pass
        elif textx:
            device = textx.text
        else:
            await request.edit("`Usage: .device <codename> / <model>`")
            return
        found = [i for i in get(DEVICES_DATA).json()
                 if i["device"] == device or i["model"] == device]
        if found:
            reply = f'Search results for {device}:\n'
            for item in found:
                brand = item['brand']
                name = item['name']
                codename = item['device']
                model = item['model']
                reply += f'{brand} {name}\n' \
                    f'**Codename**: `{codename}`\n' \
                    f'**Model**: {model}\n\n'
        else:
            reply = f"`Couldn't find info about {device}!`\n"
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.codename(?: |)([\S]*)(?: |)([\s\S]*)")
@errors_handler
async def codename_info(request):
    """ search for android codename """
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        brand = request.pattern_match.group(1).lower()
        device = request.pattern_match.group(2).lower()
        if brand and device:
            pass
        elif textx:
            brand = textx.text.split(' ')[0]
            device = ' '.join(textx.text.split(' ')[1:])
        else:
            await request.edit("`Usage: .codename <brand> <device>`")
            return
        found = [i for i in get(DEVICES_DATA).json(
        ) if i["brand"].lower() == brand and device in i["name"].lower()]
        if len(found) > 8:
            found = found[:8]
        if found:
            reply = f'Search results for {brand.capitalize()} {device.capitalize()}:\n'
            for item in found:
                brand = item['brand']
                name = item['name']
                codename = item['device']
                model = item['model']
                reply += f'{brand} {name}\n' \
                    f'**Codename**: `{codename}`\n' \
                    f'**Model**: {model}\n\n'
        else:
            reply = f"`Couldn't find {device} codename!`\n"
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.specs(?: |)([\S]*)(?: |)([\s\S]*)")
@errors_handler
async def devices_specifications(request):
    """ Mobile devices specifications """
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        brand = request.pattern_match.group(1).lower()
        device = request.pattern_match.group(2).lower()
        if brand and device:
            pass
        elif textx:
            brand = textx.text.split(' ')[0]
            device = ' '.join(textx.text.split(' ')[1:])
        else:
            await request.edit("`Usage: .specs <brand> <device>`")
            return
        all_brands = BeautifulSoup(
            get('https://www.devicespecifications.com/en/brand-more').content,
            'lxml').find('div',
                         {'class': 'brand-listing-container-news'}).findAll('a')
        brand_page_url = None
        try:
            brand_page_url = [i['href']
                              for i in all_brands if brand == i.text.strip().lower()][0]
        except IndexError:
            await request.edit(f'`{brand} is unknown brand!`')
        devices = BeautifulSoup(get(brand_page_url).content, 'lxml') \
            .findAll('div', {'class': 'model-listing-container-80'})
        device_page_url = None
        try:
            device_page_url = [
                i.a['href'] for i in BeautifulSoup(
                    str(devices),
                    'lxml') .findAll('h3') if device in i.text.strip().lower()]
        except IndexError:
            await request.edit(f"`can't find {device}!`")
        if len(device_page_url) > 2:
            device_page_url = device_page_url[:2]
        reply = ''
        for url in device_page_url:
            info = BeautifulSoup(get(url).content, 'lxml')
            reply = '\n' + info.title.text.split('-')[0].strip() + '\n'
            info = info.find('div', {'id': 'model-brief-specifications'})
            specifications = re.findall(r'<b>.*?<br/>', str(info))
            for item in specifications:
                title = re.findall(r'<b>(.*?)</b>', item)[0].strip()
                data = re.findall(r'</b>: (.*?)<br/>', item)[0]\
                    .replace('<b>', '').replace('</b>', '').strip()
                reply += f'**{title}**: {data}\n'
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.twrp(?: |$)(\S*)")
@errors_handler
async def twrp(request):
    """ get android device twrp """
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        device = request.pattern_match.group(1)
        if device:
            pass
        elif textx:
            device = textx.text.split(' ')[0]
        else:
            await request.edit("`Usage: .twrp <codename>`")
            return
        url = get(f'https://dl.twrp.me/{device}/')
        if url.status_code == 404:
            reply = f"`Couldn't find twrp downloads for {device}!`\n"
            await request.edit(reply)
            return
        page = BeautifulSoup(url.content, 'lxml')
        download = page.find('table').find('tr').find('a')
        dl_link = f"https://dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        reply = f'**Latest TWRP for {device}:**\n' \
            f'[{dl_file}]({dl_link}) - __{size}__\n' \
            f'**Updated:** __{date}__\n'
        await request.edit(reply)

CMD_HELP.update({
    "magisk": "Get latest Magisk releases"
})
CMD_HELP.update({
    "device": ".device <codename>\nUsage: Get info about android device codename or model."
})
CMD_HELP.update({
    "codename": ".codename <brand> <device>\nUsage: Search for android device codename."
})
CMD_HELP.update({
    "specs": ".specs <brand> <device>\nUsage: Get device specifications info."
})
CMD_HELP.update({
    "twrp": ".twrp <codename>\nUsage: Get latest twrp download for android device."
})

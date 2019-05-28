# Copyright (C) 2019 Rupansh Sekar
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from io import BytesIO
from random import randint
import requests
import xml.etree.ElementTree as xmlET

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.r34")
async def r34(tags):
    if not tags.text[0].isalpha() and tags.text[0] not in ("/", "#", "@", "!"):
        BASE_URL= "https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=20"
        passtags = tags.text.split(" ", 1)[1].split()
        paramdict = {"tags": []}

        for tag in passtags:
            paramdict["tags"].append(tag)

        xmlresp = requests.get(BASE_URL, paramdict)
        if xmlresp.status_code == requests.codes.ok:
            toproc = xmlET.fromstring(xmlresp.content)
            imglist = [url.attrib['file_url'] for url in toproc]

            imgreq = requests.get(imglist[randint(0, len(imglist)-1)], stream=True)
            buf = BytesIO()
            buf.name = "hentai.jpeg"
            for chunk in imgreq.iter_content(chunk_size=128):
                buf.write(chunk)
            buf.seek(0)

            img = await tags.client.upload_file(buf)

            await tags.client.send_file(tags.chat_id, img)
            await tags.delete()
        else:
            tags.edit(f"`Error from rule34 with error code {xmlresp.status_code}`")


CMD_HELP.update({
    "r34" : """.r34
    Usage: send tags after .r34 in the rule34 format
    Checkout the rule34 cheatsheet here - https://rule34.xxx/index.php?page=help&topic=cheatsheet for tag usage"""})


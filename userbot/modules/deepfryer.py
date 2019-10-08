# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Original source for the deepfrying code (used under the following license): https://github.com/Ovyerus/deeppyer

# MIT License
#
# Copyright (c) 2017 Ovyerus
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
""" Userbot module for frying stuff. """

import io

from PIL import Image, ImageEnhance, ImageOps

from userbot import CMD_HELP, bot
from userbot.events import errors_handler, register


@register(outgoing=True, pattern="deepfry")
@errors_handler
async def deepfryer(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = reply_message.photo
        data2 = reply_message.sticker
    else:
        data = None
        data2 = None

    # check if message does contain media and cancel when not
    if not data and not data2:
        await event.edit("`I need an image or sticker to deep fry!`")
        return

    # download last photo (highres) as byte array
    if data:
        image = io.BytesIO()
        image = await bot.download_media(data, image)
        image = Image.open(image)
    elif data2:
        image = io.BytesIO()
        image = await bot.download_media(data2, image)
        image = Image.open(image)

    # fry the image
    fried_image = await deepfry(image)
    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    fried_image.save(fried_io, "JPEG")
    fried_io.seek(0)

    await event.reply(file=fried_io)


async def deepfry(img: Image) -> Image:
    colours = ((50, 30, 40), (255, 240, 245))
    img = img.copy().convert("RGB")

    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize((int(width ** .85), int(height ** .85)), resample=Image.LANCZOS)
    img = img.resize((int(width ** .92), int(height ** .92)), resample=Image.BILINEAR)
    img = img.resize((int(width ** .97), int(height ** .97)), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, 7)

    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(1.2)
    overlay = ImageEnhance.Brightness(overlay).enhance(1.0)

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, 0.15)
    img = ImageEnhance.Sharpness(img).enhance(300)

    return img


CMD_HELP.update({
    'deepfry':
    ".deepfry"
    "\nDeepfries an image or sticker."
})

from telethon import events
from userbot import bot 
from userbot.events import register
import asyncio
import requests


@register(outgoing=True, pattern="^.kod (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    DELIMITER = "|"
    if DELIMITER not in input_str:
        await event.edit("Invalid Syntax")
        return False
    lang, code = input_str.split(DELIMITER)
    url = "http://apikuu.herokuapp.com/api/v0/sakty/karbon"
    a = requests.get(url, params={
        "code": code,
        "lang": lang,
        "line": True
    }).json()
    img_url = a["hasil"]["karbon"]
    reply_message_id = event.message.id
    if event.reply_to_msg_id:
        reply_message_id = event.reply_to_msg_id
    try:
        await bot.send_file(
            event.chat_id,
            img_url,
            caption=code,
            force_document=False,
            allow_cache=False,
            reply_to=reply_message_id
        )
        await event.delete()
    except Exception as e:
        await event.edit(str(e))


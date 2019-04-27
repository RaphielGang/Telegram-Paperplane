from telethon import events
from userbot import bot
import random
import asyncio


@bot.on(events.NewMessage(pattern=r"\.schd ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    ttl = 0
    message = "SYNTAX: `.schd <time_in_seconds> ;=; <message to send>`"
    if input_str:
        await event.delete()
        if ";=;" in input_str:
            ttl, message = input_str.split(";=;")
        elif event.reply_to_msg_id:
            await event.delete()
            ttl = int(input_str)
            message = await event.get_reply_message()
        await asyncio.sleep(int(ttl))
        await event.respond(message)
    else:
        await event.edit(message)


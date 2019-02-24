import asyncio, subprocess
import time
from userbot import bot, LOGGER, LOGGER_GROUP
from telethon import events
from telethon.events import StopPropagation
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.channels import LeaveChannelRequest, CreateChannelRequest, DeleteMessagesRequest
from lmgtfy import lmgtfy

@bot.on(events.NewMessage(outgoing=True, pattern="^.leave$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.leave$"))
async def leave(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`I iz Leaving dis Group kek!`")
        time.sleep(3)
        if '-' in str(e.chat_id):
            await bot(LeaveChannelRequest(e.chat_id))
        else:
            await e.edit('`Sar This is Not A Chat`')

@bot.on(events.NewMessage(pattern="^.lmg", outgoing=True))
@bot.on(events.MessageEdited(pattern="^.lmg", outgoing=True))
async def let_me_google_that_for_you(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = e.text
        if message[8:]:
            message = str(message[8:])
        elif textx:
            message = str(textx.message)
        reply_text = 'http://lmgtfy.com/?s=g&iie=1&q=' + message.replace(" ", "+")
        await e.edit(reply_text)
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                "LMGTFY query " + message + " was executed successfully",
            )

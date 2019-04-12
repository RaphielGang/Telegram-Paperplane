import asyncio, subprocess
import time
from userbot import bot, LOGGER, LOGGER_GROUP
from telethon import events, functions, types
from telethon.events import StopPropagation
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.channels import LeaveChannelRequest, CreateChannelRequest, DeleteMessagesRequest
from lmgtfy import lmgtfy
from collections import deque
from telethon.tl.functions.users import GetFullUserRequest

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

@bot.on(events.NewMessage(outgoing=True, pattern="^;__;$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^;__;$"))
async def fun(e):
    t = ";__;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)


@bot.on(events.NewMessage(outgoing=True, pattern="^.cry$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.cry$"))
async def cry(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("(;´༎ຶД༎ຶ)")

@bot.on(events.NewMessage(outgoing=True, pattern="^.fp$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.fp$"))
async def facepalm(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("🤦‍♂")

@bot.on(events.NewMessage(pattern=r"\.moon animation", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
	for _ in range(32):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

@bot.on(events.NewMessage(outgoing=True, pattern="^.sauce$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sauce$"))
async def source(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/Yasir-siddiqui/Userbot/")

@bot.on(events.NewMessage(outgoing=True, pattern="^.readme$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.readme$"))
async def reedme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/Yasir-siddiqui/UserBot/blob/master/README.md")

@bot.on(events.NewMessage(outgoing=True, pattern="^.disapprove$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.disapprove$"))
async def disapprovepm(disapprvpm):
    if not disapprvpm.text[0].isalpha() and disapprvpm.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.pm_permit_sql import dissprove
        except:
            await disapprvpm.edit("`Running on Non-SQL mode!`")
            return

        if disapprvpm.reply_to_msg_id:
            reply = await disapprvpm.get_reply_message()
            replied_user = await bot(GetFullUserRequest(reply.from_id))
            aname = replied_user.user.id
            name0 = str(replied_user.user.first_name)
            dissprove(replied_user.user.id)
        else:
            dissprove(disapprvpm.chat_id)
            aname = await bot.get_entity(disapprvpm.chat_id)
            name0 = str(aname.first_name)

        await disapprvpm.edit(
            f"[{name0}](tg://user?id={disapprvpm.chat_id}) `Disaproved to PM!`"
            )

        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP,
                f"[{name0}](tg://user?id={disapprvpm.chat_id})"
                " was disapproved to PM you.",
            )

@bot.on(events.NewMessage(pattern=r"\.clock animation", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
	for _ in range(32):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

@bot.on(events.NewMessage(pattern=r"\.myusernames", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    result = await bot(functions.channels.GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    await event.edit(output_str)


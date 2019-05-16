import asyncio, subprocess
import time, re, io, os
from userbot import bot, LOGGER, LOGGER_GROUP, HELPER
from telethon import events, functions, types
from telethon.events import StopPropagation
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.channels import LeaveChannelRequest, CreateChannelRequest, DeleteMessagesRequest
from lmgtfy import lmgtfy
from collections import deque
from telethon.tl.functions.users import GetFullUserRequest
from userbot.events import register
from userbot.modules.rextester.api import UnknownLanguage, Rextester
from time import sleep
from selenium import webdriver
from urllib.parse import quote_plus
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

@register(outgoing=True, pattern="^.leave$")
async def leave(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`I iz Leaving dis Group kek!`")
        time.sleep(3)
        if '-' in str(e.chat_id):
            await bot(LeaveChannelRequest(e.chat_id))
        else:
            await e.edit('`Sar This is Not A Chat`')

@register(outgoing=True, pattern="^;__;$")
async def fun(e):
    t = ";__;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)

@register(outgoing=True, pattern="^Oof$")
async def Oof(e):
    t = "Oof"
    for j in range(15):
        t = t[:-1] + "of"
        await e.edit(t)

@register(outgoing=True, pattern="^.cry$")
async def cry(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("(;´༎ຶД༎ຶ)")

@register(outgoing=True, pattern="^.fp$")
async def facepalm(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("🤦‍♂")

@register(outgoing=True, pattern="^.moon$")
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
	for _ in range(32):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

@register(outgoing=True, pattern="^.sauce$")
async def source(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/Yasir-siddiqui/Userbot/")

@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("https://github.com/Yasir-siddiqui/UserBot/blob/master/README.md")

@register(outgoing=True, pattern="^.disapprove$")
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

@register(outgoing=True, pattern="^.clock$")
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
	for _ in range(32):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)

@register(outgoing=True, pattern="^.myusernames$")
async def _(event):
    if event.fwd_from:
        return
    result = await bot(functions.channels.GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    await event.edit(output_str)

@register(outgoing=True, pattern="^\$")
async def rextestercli(e):
    stdin = ""
    message = e.text
    chat = await e.get_chat()

    if len(message.split()) > 1:
        regex = re.search(
            r"^\$([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$",
            message,
            re.IGNORECASE,
        )
        language = regex.group(1)
        code = regex.group(2)
        stdin = regex.group(3)

        try:
            rextester = Rextester(language, code, stdin)
            res = await rextester.exec()
        except UnknownLanguage as exc:
            await e.edit(str(exc))
            return

        output = ""
        output += f"**Language:**\n```{language}```"
        output += f"\n\n**Source:** \n```{code}```"

        if res.result:
            output += f"\n\n**Result:** \n```{res.result}```"

        if res.warnings:
            output += f"\n\n**Warnings:** \n```{res.warnings}```\n"

        if res.errors:
            output += f"\n\n**Errors:** \n'```{res.errors}```"

        if len(res.result) > 4096:
            with io.BytesIO(str.encode(res.result)) as out_file:
                out_file.name = "result.txt"
                await bot.send_file(chat.id, file = out_file)
                await e.edit(code)
            return

        await e.edit(output)


@register(outgoing=True, pattern="^.setlang")
async def setlang(prog):
    if not prog.text[0].isalpha() and prog.text[0] not in ("/", "#", "@", "!"):
        global LANG
        LANG = prog.text.split()[1]
        await prog.edit(f"language set to {LANG}")


@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Processing...")
        CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
        LANG = "en"
        textx = await e.get_reply_message()
        pcode = e.text
        if pcode[8:]:
            pcode = str(pcode[8:])
        elif textx:
            pcode = str(textx.message)  # Importing message to module
        code = quote_plus(pcode)  # Converting to urlencoded
        url = CARBON.format(code=code, lang=LANG)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')
        prefs = {'download.default_directory': '/'}
        chrome_options.add_experimental_option('prefs', prefs)
        await e.edit("Processing 30%")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        download_path = '/home/'
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
        command_result = driver.execute("send_command", params)

        driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
        sleep(3)  # this might take a bit.
        await e.edit("Processing 50%")
        driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
        sleep(3)  # Waiting for downloading

        await e.edit("Processing 90%")
        file = '/home/carbon.png'
        await e.edit("Done!!")
        await bot.send_file(
         e.chat_id,
         file,
         reply_to=e.message.reply_to_msg_id,
           )

    os.remove('/home/carbon.png')
   # Removing carbon.png after uploading
    await e.delete()

HELPER.update({
      "carbon":".carbon <text> \n Beautify your code"
})
HELPER.update({
    'setlang': ".setlang <Lang> \
            \nUsage: It will set language for you carbon module "
})
HELPER.update({
    "leave": "Leave a Chat"
})
HELPER.update({
    ";__;": "You try it!"
})
HELPER.update({
    "cry": "Cry"
})
HELPER.update({
    "fp": "Send face palm emoji."
})
HELPER.update({
    "moon": "Bot will send a cool moon animation."
})
HELPER.update({
    "clock": "Bot will send a cool clock animation."
})
HELPER.update({
    "readme": "Reedme."
})
HELPER.update({
    "sauce": "source."
})
HELPER.update({
    "disapprove": "Disapprove anyone in PM."
})
HELPER.update({
    "myusernames": "List of Usernames owned by you."
})
HELPER.update({
    "oof": "Same as ;__; but ooof"
})

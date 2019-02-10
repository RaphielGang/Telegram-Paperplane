import subprocess
from datetime import datetime

from telethon import events, functions

from userbot import bot


@bot.on(events.NewMessage(outgoing=True, pattern="^.speed$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.speed$"))
async def speedtest(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        l = await e.reply("`Running speed test . . .`")
        k = subprocess.run(["speedtest-cli --simple"], stdout=subprocess.PIPE)
        await l.edit("`" + k.stdout.decode()[:-1] + "`")
        await e.delete()

@bot.on(events.NewMessage(outgoing=True, pattern="^.nearestdc$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.nearestdc$"))
async def neardc(e):
    result = await bot(functions.help.GetNearestDcRequest())
    await e.edit(
        f"Country : `{result.country}` \n"
        f"Nearest Datacenter : `{result.nearest_dc}` \n"
        f"This Datacenter : `{result.this_dc}`"
    )

@bot.on(events.NewMessage(outgoing=True, pattern="^.pingme$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.pingme$"))
async def pingme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        start = datetime.now()
        await e.edit("`Pong!`")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await e.edit("Pong!\n%sms" % (ms))

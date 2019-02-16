import subprocess
import speedtest

from datetime import datetime

from telethon import events, functions

from userbot import bot


@bot.on(events.NewMessage(outgoing=True, pattern="^.speed$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.speed$"))
async def speedtst(spd):
    if not spd.text[0].isalpha() and spd.text[0] not in ("/", "#", "@", "!"):
        await spd.edit("`Running speed test . . .`")
        test = speedtest.Speedtest()

        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()

    await spd.edit("`"
                   "Started at "
                   f"{result['timestamp']} \n\n"
                   "Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {
        0: '',
        1: 'KB',
        2: 'MB',
        3: 'GB',
        4: 'TB'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


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

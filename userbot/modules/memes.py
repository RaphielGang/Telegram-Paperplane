import asyncio
import random
import re
import time

from spongemock import spongemock
from telethon import TelegramClient, events
from zalgo_text import zalgo

from userbot import (DISABLE_RUN, ENABLE_KILLME, LOGGER, LOGGER_GROUP,
                     WIDE_MAP, bot)


@bot.on(events.NewMessage(outgoing=True, pattern="^:/$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^:/$"))
async def kek(keks):
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@bot.on(events.NewMessage(outgoing=True, pattern="^-_-$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^-_-$"))
async def lol(lel):
    ok = "-_-"
    if range(10):
        ok = t[:-1] + "_-"
        await lel.edit(t)


@bot.on(events.NewMessage(outgoing=True, pattern="^.cp"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.cp"))
async def copypasta(cp):
    if not cp.text[0].isalpha() and cp.text[0] not in ("/", "#", "@", "!"):
        textx = await cp.get_reply_message()
        message = cp.text
        if message[3:]:
            message = str(message[3:])
        elif textx:
            message = textx
            message = str(message.message)
        emojis = [
            "😂",
            "😂",
            "👌",
            "✌",
            "💞",
            "👍",
            "👌",
            "💯",
            "🎶",
            "👀",
            "😂",
            "👓",
            "👏",
            "👐",
            "🍕",
            "💥",
            "🍴",
            "💦",
            "💦",
            "🍑",
            "🍆",
            "😩",
            "😏",
            "👉👌",
            "👀",
            "👅",
            "😩",
            "🚰",
        ]
        reply_text = random.choice(emojis)
        b_char = random.choice(
            message
        ).lower()  # choose a random character in the message to be substituted with 🅱️
        for owo in message:
            if owo == " ":
                reply_text += random.choice(emojis)
            elif owo in emojis:
                reply_text += owo
                reply_text += random.choice(emojis)
            elif owo.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += owo.upper()
                else:
                    reply_text += owo.lower()
        reply_text += random.choice(emojis)
        await cp.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.vapor (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.vapor (.*)"))
async def vapor(vpr):
    if not vpr.text[0].isalpha() and vpr.text[0] not in ("/", "#", "@", "!"):
        textx = await vpr.get_reply_message()
        message = vpr.text
        if message[7:]:
            message = vpr.pattern_match.group(1)
        elif textx:
            message = textx
            message = str(message.message)
        if message:
            data = message
        else:
            data = ""
        reply_text = str(data).translate(WIDE_MAP)
        await vpr.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.str (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.str (.*)"))
async def stretch(stret):
    if not stret.text[0].isalpha() and stret.text[0] not in ("/", "#", "@", "!"):
        textx = await stret.get_reply_message()
        message = stret.text
        if message[5:]:
            message = stret.pattern_match.group(1)
        elif textx:
            message = textx
            message = str(message.message)
        count = random.randint(3, 10)
        reply_text = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
            (r"\1"*count),
            message
            )
        await stret.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.zal (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.zal (.*)"))
async def zal(zgfy):
    if not zgfy.text[0].isalpha() and zgfy.text[0] not in ("/", "#", "@", "!"):
        textx = await zgfy.get_reply_message()
        message = zgfy.text
        if message[4:]:
            message = zgfy.pattern_match.group(1)
        elif textx:
            message = textx
            message = str(message.message)
        input_text = " ".join(message).lower()
        zalgofied_text = zalgo.zalgo().zalgofy(input_text)
        await zgfy.edit(zalgofied_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^hi$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^hi$"))
async def hoi(ha):
    await ha.edit("Hoi!😄")


@bot.on(events.NewMessage(outgoing=True, pattern="^.owo (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.owo (.*)"))
async def faces(owo):
    if not owo.text[0].isalpha() and owo.text[0] not in ("/", "#", "@", "!"):
        textx = await owo.get_reply_message()
        message = owo.text
        if message[5:]:
            message = owo.pattern_match.group(1)
        elif textx:
            message = textx
            message = str(message.message)
        uwus = [
            "(・`ω´・)",
            ";;w;;",
            "owo",
            "UwU",
            ">w<",
            "^w^",
            r"\(^o\) (/o^)/",
            "( ^ _ ^)∠☆",
            "(ô_ô)",
            "~:o",
            ";-;",
            "(*^*)",
            "(>_",
            "(♥_♥)",
            "*(^O^)*",
            "((+_+))",
        ]
        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(uwus), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(uwus)
        await owo.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.react$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.react$"))
async def react_meme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        reactor = [
            "ʘ‿ʘ",
            "ヾ(-_- )ゞ",
            "(っ˘ڡ˘ς)",
            "(´ж｀ς)",
            "( ಠ ʖ̯ ಠ)",
            "(° ͜ʖ͡°)╭∩╮",
            "(ᵟຶ︵ ᵟຶ)",
            "(งツ)ว",
            "ʚ(•｀",
            "(っ▀¯▀)つ",
            "(◠﹏◠)",
            "( ͡ಠ ʖ̯ ͡ಠ)",
            "( ఠ ͟ʖ ఠ)",
            "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
            "(⊃｡•́‿•̀｡)⊃",
            "(._.)",
            "{•̃_•̃}",
            "(ᵔᴥᵔ)",
            "♨_♨",
            "⥀.⥀",
            "ح˚௰˚づ ",
            "(҂◡_◡)",
            "ƪ(ړײ)‎ƪ​​",
            "(っ•́｡•́)♪♬",
            "◖ᵔᴥᵔ◗ ♪ ♫ ",
            "(☞ﾟヮﾟ)☞",
            "[¬º-°]¬",
            "(Ծ‸ Ծ)",
            "(•̀ᴗ•́)و ̑̑",
            "ヾ(´〇`)ﾉ♪♪♪",
            "(ง'̀-'́)ง",
            "ლ(•́•́ლ)",
            "ʕ •́؈•̀ ₎",
            "♪♪ ヽ(ˇ∀ˇ )ゞ",
            "щ（ﾟДﾟщ）",
            "( ˇ෴ˇ )",
            "눈_눈",
            "(๑•́ ₃ •̀๑) ",
            "( ˘ ³˘)♥ ",
            "ԅ(≖‿≖ԅ)",
            "♥‿♥",
            "◔_◔",
            "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
            "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
            "( ఠൠఠ )ﾉ",
            "٩(๏_๏)۶",
            "┌(ㆆ㉨ㆆ)ʃ",
            "ఠ_ఠ",
            "(づ｡◕‿‿◕｡)づ",
            "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
            "“ヽ(´▽｀)ノ”",
            "༼ ༎ຶ ෴ ༎ຶ༽",
            "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
            "(づ￣ ³￣)づ",
            "(⊙.☉)7",
            "ᕕ( ᐛ )ᕗ",
            "t(-_-t)",
            "(ಥ⌣ಥ)",
            "ヽ༼ ಠ益ಠ ༽ﾉ",
            "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
            "ミ●﹏☉ミ",
            "(⊙_◎)",
            "¿ⓧ_ⓧﮌ",
            "ಠ_ಠ",
            "(´･_･`)",
            "ᕦ(ò_óˇ)ᕤ",
            "⊙﹏⊙",
            "(╯°□°）╯︵ ┻━┻",
            r"¯\_(⊙︿⊙)_/¯",
            "٩◔̯◔۶",
            "°‿‿°",
            "ᕙ(⇀‸↼‶)ᕗ",
            "⊂(◉‿◉)つ",
            "V•ᴥ•V",
            "q(❂‿❂)p",
            "ಥ_ಥ",
            "ฅ^•ﻌ•^ฅ",
            "ಥ﹏ಥ",
            "（ ^_^）o自自o（^_^ ）",
            "ಠ‿ಠ",
            "ヽ(´▽`)/",
            "ᵒᴥᵒ#",
            "( ͡° ͜ʖ ͡°)",
            "┬─┬﻿ ノ( ゜-゜ノ)",
            "ヽ(´ー｀)ノ",
            "☜(⌒▽⌒)☞",
            "ε=ε=ε=┌(;*´Д`)ﾉ",
            "(╬ ಠ益ಠ)",
            "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
            "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
            r"¯\_(ツ)_/¯",
            "ʕᵔᴥᵔʔ",
            "(`･ω･´)",
            "ʕ•ᴥ•ʔ",
            "ლ(｀ー´ლ)",
            "ʕʘ̅͜ʘ̅ʔ",
            "（　ﾟДﾟ）",
            r"¯\(°_o)/¯",
            "(｡◕‿◕｡)",
        ]
        index = random.randint(0, len(reactor))
        reply_text = reactor[index]
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.shg$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.shg$"))
async def shrugger(shg):
    if not shg.text[0].isalpha() and shg.text[0] not in ("/", "#", "@", "!"):
        await shg.edit(r"¯\_(ツ)_/¯")


@bot.on(events.NewMessage(outgoing=True, pattern="^.runs$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.runs$"))
async def runner_lol(run):
    if not DISABLE_RUN:
        if not run.text[0].isalpha() and run.text[0] not in ("/", "#", "@", "!"):
            reactor = [
                "Runs to Thanos",
                "Runs far, far away from earth",
                "Running faster than usian bolt coz I'mma Bot",
                "Runs to Marie",
                "This Group is too cancerous to deal with.",
                "Cya bois",
                "Kys",
                "I am a mad person. Plox Ban me.",
                "I go away",
                "I am just walking off, coz me is too fat.",
                "I Fugged off!",
            ]
            index = random.randint(0, len(reactor) - 1)
            reply_text = reactor[index]
            await run.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.disable runs$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.disable runs$"))
async def disable_killme(nokill):
    if not nokill.text[0].isalpha() and nokill.text[0] not in ("/", "#", "@", "!"):
        global DISABLE_RUN
        DISABLE_RUN = True
        await nokill.edit("```Done!```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.enable runs$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.enable runs$"))
async def enable_killme(killme):
    if not killme.text[0].isalpha() and killme.text[0] not in ("/", "#", "@", "!"):
        global DISABLE_RUN
        DISABLE_RUN = False
        await killme.edit("```Done!```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.metoo"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.metoo"))
async def metoo(hahayes):
    if not hahayes.text[0].isalpha() and hahayes.text[0] not in ("/", "#", "@", "!"):
        metoostr = [
            "Me too thanks",
            "Haha yes, me too",
            "Same lol",
            "Me irl",
            "Same here",
            "Haha yes",
            "Me rn",
        ]
        index = random.randint(0, len(metoostr) - 1)
        reply_text = metoostr[index]
        await hahayes.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.mock"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.mock"))
async def spongemocktext(mock):
    if not mock.text[0].isalpha() and mock.text[0] not in ("/", "#", "@", "!"):
        textx = await mock.get_reply_message()
        message = mock.text
        if message[6:]:
            message = str(message[6:])
        elif textx:
            message = textx
            message = str(message.message)
        reply_text = spongemock.mock(message)
        await mock.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.clap (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.clap (.*)"))
async def claptext(memereview):
    textx = await memereview.get_reply_message()
    message = memereview.text
    if message[6:]:
        message = memereview.pattern_match.group(1)
    elif textx:
        message = textx
        message = str(message.message)
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.bt$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.bt$"))
async def bluetext(bt):
    if await bt.get_reply_message():
        await bt.edit(
            "`BLUETEXT MUST CLICK.`\n"
            "`Are you a stupid animal which is attracted to colours?`"
        )


@bot.on(events.NewMessage(pattern='(?i).type'))
@bot.on(events.MessageEdited(pattern='(?i).type'))
async def typewriter(typew):
    if not typew.text[0].isalpha() and typew.text[0] not in ("/", "#", "@", "!"):
        textx = await typew.get_reply_message()
        message = typew.text

        if message[6:]:
            message = str(message[6:])
        elif textx:
            message = textx
            message = str(message.message)
        sleep_time = 0.03
        typing_symbol = "|"
        old_text = ''
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)

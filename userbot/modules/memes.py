from zalgo_text import zalgo
import random, re
from userbot import bot, ENABLE_KILLME, WIDE_MAP
from userbot import LOGGER, LOGGER_GROUP, DISABLE_RUN
from telethon import TelegramClient, events
from spongemock import spongemock
import time


@bot.on(events.NewMessage(outgoing=True, pattern="^:/$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^:/$"))
async def kek(e):
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await e.edit(":" + uio[i % 2])


@bot.on(events.NewMessage(outgoing=True, pattern="^-_-$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^-_-$"))
async def lol(e):
    t = "-_-"
    for j in range(10):
        t = t[:-1] + "_-"
        await e.edit(t)


@bot.on(events.NewMessage(outgoing=True, pattern="^.cp"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.cp"))
async def copypasta(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message=e.text
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
        for c in message:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.vapor"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.vapor"))
async def vapor(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = e.text
        if message[7:]:
            message = str(message[7:])
        elif textx:
            message = textx
            message = str(message.message)
        if message:
            data = message
        else:
            data = ""
        reply_text = str(data).translate(WIDE_MAP)
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.str"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.str"))
async def stretch(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = e.text
        if message[5:]:
            message = str(message[5:])
        elif textx:
            message = textx
            message = str(message.message)
        count = random.randint(3, 10)
        reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), message)
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.zal"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.zal"))
async def zal(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = e.text
        if message[4:]:
            message = str(message[4:])
        elif textx:
            message = textx
            message = str(message.message)
        input_text = " ".join(message).lower()
        zalgofied_text = zalgo.zalgo().zalgofy(input_text)
        await e.edit(zalgofied_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^hi$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^hi$"))
async def hoi(e):
    await e.edit("Hoi!😄")


@bot.on(events.NewMessage(outgoing=True, pattern="^.owo"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.owo"))
async def faces(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message=e.text
        if message[5:]:
            message = str(message[5:])
        elif textx:
            message = textx
            message = str(message.message)
        faces = [
            "(・`ω´・)",
            ";;w;;",
            "owo",
            "UwU",
            ">w<",
            "^w^",
            "\(^o\) (/o^)/",
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
        reply_text = re.sub(r"\!+", " " + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(faces)
        await e.edit(reply_text)


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
            "¯\_(⊙︿⊙)_/¯",
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
            "¯\_(ツ)_/¯",
            "ʕᵔᴥᵔʔ",
            "(`･ω･´)",
            "ʕ•ᴥ•ʔ",
            "ლ(｀ー´ლ)",
            "ʕʘ̅͜ʘ̅ʔ",
            "（　ﾟДﾟ）",
            "¯\(°_o)/¯",
            "(｡◕‿◕｡)",
        ]
        index = random.randint(0, len(reactor))
        reply_text = reactor[index]
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.shg$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.shg$"))
async def shrugger(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("¯\_(ツ)_/¯")


@bot.on(events.NewMessage(outgoing=True, pattern="^.runs$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.runs$"))
async def runner_lol(e):
    if not DISABLE_RUN:
        if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
            reactor = [
                "Runs to Thanos",
                "Runs far, far away from earth",
                "Running faster than usian bolt coz I'mma Bot",
                "Runs to Marie",
                "This Group is too cancerous to deal with.",
                "Cya bois",
                "I am just retarded",
                "Kys",
                "I am a mad person. Plox Ban me.",
                "I go away",
                "I am just walking off, coz me is too fat.",
                "I Fugged off!",
            ]
            index = random.randint(0, len(reactor) - 1)
            reply_text = reactor[index]
            await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.disable runs$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.disable runs$"))
async def disable_killme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global DISABLE_RUN
        DISABLE_RUN = True
        await e.edit("```Done!```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.enable runs$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.enable runs$"))
async def enable_killme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global DISABLE_RUN
        DISABLE_RUN = False
        await e.edit("```Done!```")


@bot.on(events.NewMessage(outgoing=True, pattern="^.metoo"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.metoo"))
async def metoo(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
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
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.mock"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.mock"))
async def spongemocktext(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        textx = await e.get_reply_message()
        message = e.text
        if message[6:]:
            message = str(message[6:])
        elif textx:
            message = textx
            message = str(message.message)
        reply_text = spongemock.mock(message)
        await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.clap"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.clap"))
async def claptext(e):
    textx = await e.get_reply_message()
    message = e.text
    if message[6:]:
        message = str(message[6:])
    elif textx:
        message = textx
        message = str(message.message)
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await e.edit(reply_text)


@bot.on(events.NewMessage(outgoing=True, pattern="^.bt$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.bt$"))
async def bluetext(e):
    if await e.get_reply_message():
        await e.edit(
            "`BLUETEXT MUST CLICK.\nAre you a stupid animal which is attracted to colours?`"
        )

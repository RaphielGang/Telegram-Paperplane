from zalgo_text import zalgo
import random,re
@bot.on(events.NewMessage(outgoing=True, pattern=':/'))
@bot.on(events.MessageEdited(outgoing=True, pattern=':/'))
async def kek(e):
    uio=['/','\\']
    for i in range (1,15):
        time.sleep(0.3)
        await e.edit(':'+uio[i%2])
@bot.on(events.NewMessage(outgoing=True, pattern='-_-'))
@bot.on(events.MessageEdited(outgoing=True, pattern='-_-'))
async def lol(e):
    await e.delete()
    t = '-_-'
    r = await e.reply(t)
    for j in range(10):
        t = t[:-1] + '_-'
        await r.edit(t)
@bot.on(events.NewMessage(outgoing=True, pattern='.cp'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.cp'))
async def copypasta(e):
    textx=await e.get_reply_message()
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = e.text
        message = str(message[3:])
    emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
    reply_text = random.choice(emojis)
    b_char = random.choice(message).lower() # choose a random character in the message to be substituted with 🅱️
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
@bot.on(events.NewMessage(outgoing=True, pattern='.vapor'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.vapor'))
async def vapor(e):
    textx=await e.get_reply_message()
    message = e.text
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[7:])
    if message:
        data = message
    else:
        data = ''
    reply_text = str(data).translate(WIDE_MAP)
    await e.edit(reply_text)
@bot.on(events.NewMessage(outgoing=True, pattern='.str'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.str'))
async def stretch(e):
    textx=await e.get_reply_message()
    message = e.text
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[5:])
    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message)
    await e.edit(reply_text)
@bot.on(events.NewMessage(outgoing=True, pattern='.zal'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.zal'))
async def zal(e):
     textx=await e.get_reply_message()
     message = e.text
     if textx:
         message = textx
         message = str(message.message)
     else:
        message = str(message[4:])
     input_text = " ".join(message).lower()
     zalgofied_text = zalgo.zalgo().zalgofy(input_text)
     await e.edit(zalgofied_text)
@bot.on(events.NewMessage(outgoing=True,pattern="hi"))
@bot.on(events.MessageEdited(outgoing=True,pattern="hi"))
async def hoi(e):
    if e.text=="hi":
     await e.edit("Hoi!😄")
@bot.on(events.NewMessage(outgoing=True,pattern='.owo'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.owo'))
async def faces(e):
    textx=await e.get_reply_message()
    message = e.text
    if textx:
         message = textx
         message = str(message.message)
    else:
        message = str(message[4:])
    faces = ['(・`ω´・)',';;w;;','owo','UwU','>w<','^w^','\(^o\) (/o^)/','( ^ _ ^)∠☆','(ô_ô)','~:o',';-;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']
    reply_text = re.sub(r'(r|l)', "w", message)
    reply_text = re.sub(r'(R|L)', 'W', reply_text)
    reply_text = re.sub(r'n([aeiou])', r'ny\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += ' ' + random.choice(faces)
    await e.edit(reply_text)
@bot.on(events.NewMessage(outgoing=True,pattern='.react'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.react'))
async def react_meme(e):
    reactor=['ʘ‿ʘ','ヾ(-_- )ゞ','(っ˘ڡ˘ς)','(´ж｀ς)','( ಠ ʖ̯ ಠ)','(° ͜ʖ͡°)╭∩╮','(ᵟຶ︵ ᵟຶ)','(งツ)ว','ʚ(•｀','(っ▀¯▀)つ','(◠﹏◠)','( ͡ಠ ʖ̯ ͡ಠ)','( ఠ ͟ʖ ఠ)','(∩｀-´)⊃━☆ﾟ.*･｡ﾟ','(⊃｡•́‿•̀｡)⊃','(._.)','{•̃_•̃}','(ᵔᴥᵔ)','♨_♨','⥀.⥀','ح˚௰˚づ ','(҂◡_◡)','ƪ(ړײ)‎ƪ​​','(っ•́｡•́)♪♬','◖ᵔᴥᵔ◗ ♪ ♫ ','(☞ﾟヮﾟ)☞','[¬º-°]¬','(Ծ‸ Ծ)','(•̀ᴗ•́)و ̑̑','ヾ(´〇`)ﾉ♪♪♪','(ง\'̀-\'́)ง','ლ(•́•́ლ)','ʕ •́؈•̀ ₎','♪♪ ヽ(ˇ∀ˇ )ゞ','щ（ﾟДﾟщ）','( ˇ෴ˇ )','눈_눈','(๑•́ ₃ •̀๑) ','( ˘ ³˘)♥ ','ԅ(≖‿≖ԅ)','♥‿♥','◔_◔','⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾','乁( ◔ ౪◔)「      ┑(￣Д ￣)┍','( ఠൠఠ )ﾉ','٩(๏_๏)۶','┌(ㆆ㉨ㆆ)ʃ','ఠ_ఠ','(づ｡◕‿‿◕｡)づ','(ノಠ ∩ಠ)ノ彡( \\o°o)\\','“ヽ(´▽｀)ノ”','༼ ༎ຶ ෴ ༎ຶ༽','｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡','(づ￣ ³￣)づ','(⊙.☉)7','ᕕ( ᐛ )ᕗ','t(-_-t)','(ಥ⌣ಥ)','ヽ༼ ಠ益ಠ ༽ﾉ','༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽','ミ●﹏☉ミ','(⊙_◎)','¿ⓧ_ⓧﮌ','ಠ_ಠ','(´･_･`)','ᕦ(ò_óˇ)ᕤ','⊙﹏⊙','(╯°□°）╯︵ ┻━┻','¯\_(⊙︿⊙)_/¯','٩◔̯◔۶','°‿‿°','ᕙ(⇀‸↼‶)ᕗ','⊂(◉‿◉)つ','V•ᴥ•V','q(❂‿❂)p','ಥ_ಥ','ฅ^•ﻌ•^ฅ','ಥ﹏ಥ','（ ^_^）o自自o（^_^ ）','ಠ‿ಠ','ヽ(´▽`)/','ᵒᴥᵒ#','( ͡° ͜ʖ ͡°)','┬─┬﻿ ノ( ゜-゜ノ)','ヽ(´ー｀)ノ','☜(⌒▽⌒)☞','ε=ε=ε=┌(;*´Д`)ﾉ','(╬ ಠ益ಠ)','┬─┬⃰͡ (ᵔᵕᵔ͜ )','┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻','¯\_(ツ)_/¯','ʕᵔᴥᵔʔ','(`･ω･´)','ʕ•ᴥ•ʔ','ლ(｀ー´ლ)','ʕʘ̅͜ʘ̅ʔ','（　ﾟДﾟ）','¯\(°_o)/¯','(｡◕‿◕｡)']
    index=random.randint(0,len(reactor))
    reply_text=reactor[index]
    await e.edit(reply_text)
@bot.on(events.NewMessage(outgoing=True,pattern='.shg'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.shg'))
async def shrugger(e):
    await e.edit("¯\_(ツ)_/¯")
@bot.on(events.NewMessage(outgoing=True,pattern='.disable killme'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.disable killme'))
async def disable_killme(e):
        global ENABLE_KILLME
        ENABLE_KILLME=False
        await e.edit("```Done!```")
@bot.on(events.NewMessage(outgoing=True,pattern='.enable killme'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.enable killme'))
async def enable_killme(e):
            global ENABLE_KILLME
            ENABLE_KILLME=True
            await e.edit("```Done!```")
@bot.on(events.NewMessage(outgoing=True,pattern='.runs'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.runs'))
async def runner_lol(e):
    reactor=['Runs to Modi for Help','Runs to Donald Trumpet for help','Runs to Kaala','Runs to Thanos','Runs far, far away from earth','Running faster than usian bolt coz I\'mma Bot','Runs to Marie']
    index=random.randint(0,len(reactor)-1)
    reply_text=reactor[index]
    await e.edit(reply_text)
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,"You ran away from a cancerous chat")
@bot.on(events.NewMessage(incoming=True,pattern=".killme"))
async def killmelol(e):
    if ENABLE_KILLME:
         name = await bot.get_entity(e.from_id)
         name0 = str(name.first_name)
         await e.reply('**K I L L  **[' + name0 + '](tg://user?id=' + str(e.from_id) + ')**\n\nP L E A S E\n\nE N D  T H E I R  S U F F E R I N G**')

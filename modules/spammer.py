import asyncio
@bot.on(events.NewMessage(outgoing=True, pattern='.spam'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.spam'))
async def spammer(e):
    message= e.text
    counter=int(message[6:8])
    spam_message=str(e.text[8:])
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    await e.delete()
    await bot.send_message(LOGGER_GROUP,"Spam was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.bigspam'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.bigspam'))
async def bigspam(e):
    message = e.text
    counter=int(message[9:13])
    spam_message=str(e.text[13:])
    for i in range (1,counter):
       await e.respond(spam_message)
    await e.delete()
    await bot.send_message(LOGGER_GROUP,"bigspam was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.picspam'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.picspam'))
async def tiny_pic_spam(e):
    message= e.text
    TEXT=message.split()
    counter=int(TEXT[1])
    LINK=str(TEXT[2])
    for i in range (1,counter):
       await bot.send_file(e.chat_id,LINK)
    await e.delete()
    await bot.send_message(LOGGER_GROUP,"PicSpam was executed successfully")

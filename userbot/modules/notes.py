from telethon import TelegramClient, events
from userbot import bot
import sqlite3
from userbot import LOGGER, LOGGER_GROUP


@bot.on(events.NewMessage(outgoing=True, pattern='^.get notes$'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.get notes$'))
async def notes_active(e):
    if e.text[0] not in (isalpha(),'/','#','@','!'):
        from userbot.modules.sql_helper.notes_sql import get_notes
        transact="Messages saved in this chat: \n\n"
        E=get_notes(e.chat_id)
        for i in E:
            transact=transact+"🔹 "+i.keyword+"\n"
        await e.edit(transact)


@bot.on(events.NewMessage(outgoing=True, pattern='^.nosave (.*)'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.nosave (.*)'))
async def remove_notes(e):
    if e.text[0] not in (isalpha(),'/','#','@','!'):
      from userbot.modules.sql_helper.notes_sql import remove_notes
      message=e.text
      kek=message.split(" ")
      remove_notes(e.chat_id,kek[1])
      await e.edit("```Note removed successfully")


@bot.on(events.NewMessage(outgoing=True, pattern='^.addnote (.*)'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.addnote (.*)'))
async def add_filter(e):
  if not e.text[0].isalpha():
    from userbot.modules.sql_helper.notes_sql import add_note
    message=e.text
    kek=message.split()
    string=""
    for i in range(2,len(kek)):
        string=string+" "+str(kek[i])
    add_note(str(e.chat_id),kek[1],string)
    await e.edit("```Note added successfully. Use # followed by note name, to get it```")


@bot.on(events.NewMessage(incoming=True,pattern='#*'))
async def incom_note(e):
  try:
    if not (await e.get_sender()).bot:
        from userbot.modules.sql_helper.notes_sql import get_notes
        listes= e.text[1:]
        E=get_notes(e.chat_id)
        for t in E:
            if listes==t.keyword:
                await e.reply(t.reply)
                return
  except:
      pass

@bot.on(events.NewMessage(outgoing=True, pattern='^.rmnotes$'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.rmnotes$'))
async def remove_notes(e):
    if not e.text[0].isalpha():
        await e.edit("```Purging all Marie notes.```")
        time.sleep(3)
        r = await e.get_reply_message()
        filters = r.text.split('-')[1:]
        for filter in filters:
            await e.reply('/clear %s' % (filter.strip()))
            await asyncio.sleep(0.3)
        await e.respond('/save save @baalajimaestro kicked them all')
        await e.respond("```Successfully cleaned Marie notes yaay!```\n Gimme cookies @baalajimaestro")
        if LOGGER:
             await bot.send_message(LOGGER_GROUP,"I cleaned all Marie notes at "+str(e.chat_id))

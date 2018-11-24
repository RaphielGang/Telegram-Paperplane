import sqlite3
from telethon import TelegramClient, events
from userbot import bot,NULL_CHATS

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func
@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def filter_incoming_handler(e):
        from userbot.modules.sql_helper.filter_sql import get_filters
        listes= e.text.split(" ")
        for i in listes:
            E=get_filters(e.chat_id,str(i))
            if E:
                await e.reply(E.reply)
@bot.on(events.NewMessage(outgoing=True, pattern='.addfilter'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.addfilter'))
async def add_filter(e):
     from userbot.modules.sql_helper.filter_sql import add_filter
     message=e.text
     kek=message.split()
     string=""
     for i in range(2,len(kek)):
         string=string+" "+str(kek[i])
     add_filter(str(e.chat_id),kek[1],string)
     await e.edit("```Added Filter Successfully```")
@bot.on(events.NewMessage(outgoing=True, pattern='.nofilter'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.nofilter'))
async def remove_filter(e):
     from userbot.modules.sql_helper.filter_sql import remove_filter
     message=e.text
     kek=message.split(" ")
     remove_filter(e.chat_id,kek[1])

     await e.edit("```Removed Filter Successfully```")
@bot.on(events.NewMessage(outgoing=True, pattern='.rmfilters'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.rmfilters'))
async def kick_marie_filter(e):
    await e.edit("```Will be kicking away all Marie filters.```")
    time.sleep(3)
    r = await e.get_reply_message()
    filters = r.text.split('-')[1:]
    for filter in filters:
        await e.reply('/stop %s' % (filter.strip()))
        await asyncio.sleep(0.3)
    await e.respond('/filter filters @baalajimaestro kicked them all')
    await e.respond("```Successfully cleaned Marie filters yaay!```\n Gimme cookies @baalajimaestro")
    if LOGGER:
          await bot.send_message(LOGGER_GROUP,"I cleaned all Marie filters at "+str(e.chat_id))
@bot.on(events.NewMessage(outgoing=True, pattern='.get filters'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.get filters'))
async def filters_active(e):
        db=sqlite3.connect("filters.db")
        cursor=db.cursor()
        transact="Filters active on this chat: \n"
        cursor.execute('''SELECT * FROM FILTER''')
        all_rows = cursor.fetchall()
        for row in all_rows:
            if int(row[0]) == int(e.chat_id):
                    transact=transact+"-"+str(row[1])+" : "+str(row[2])+"\n"
        db.close()
        await e.edit(transact)

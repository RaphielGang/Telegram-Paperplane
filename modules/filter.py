import sqlite3
@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def filter_incoming_handler(e):
    db=sqlite3.connect("filters.db")
    cursor=db.cursor()
    cursor.execute('''SELECT * FROM FILTER''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        if int(row[0]) == int(e.chat_id):
            if str(row[1]) in str(e.text):
                await e.reply(row[2])
    db.close()
@bot.on(events.NewMessage(outgoing=True, pattern='.filter'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.filter'))
async def add_filter(e):
     message=e.text
     kek=message.split()
     db=sqlite3.connect("filters.db")
     cursor=db.cursor()
     string=""
     for i in range(2,len(kek)):
         string=string+" "+str(kek[i])
     cursor.execute('''INSERT INTO FILTER VALUES(?,?,?)''', (int(e.chat_id),kek[1],string))
     db.commit()
     await e.edit("```Added Filter Successfully```")
     db.close()
@bot.on(events.NewMessage(outgoing=True, pattern='.nofilter'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.nofilter'))
async def remove_filter(e):
     message=e.text
     kek=message.split()
     db=sqlite3.connect("filters.db")
     cursor=db.cursor()
     cursor.execute('''DELETE FROM FILTER WHERE chat_id=? AND filter=?''', (int(e.chat_id),kek[1]))
     db.commit()
     await e.edit("```Removed Filter Successfully```")
     db.close()
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

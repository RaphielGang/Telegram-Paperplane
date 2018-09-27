@bot.on(events.NewMessage(outgoing=True, pattern='.get notes'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.get notes'))
async def notes_active(e):
        db=sqlite3.connect("filters.db")
        cursor=db.cursor()
        transact="Notes active on this chat: \n"
        cursor.execute('''SELECT * FROM NOTES''')
        all_rows = cursor.fetchall()
        for row in all_rows:
            if int(row[0]) == int(e.chat_id):
                    transact=transact+"-"+str(row[1])+" : "+str(row[2])+"\n"
        db.close()
        await e.edit(transact)
@bot.on(events.NewMessage(outgoing=True, pattern='.nosave'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.nosave'))
async def remove_notes(e):
     message=e.text
     kek=message.split()
     db=sqlite3.connect("filters.db")
     cursor=db.cursor()
     cursor.execute('''DELETE FROM NOTES WHERE chat_id=? AND note=?''', (int(e.chat_id),kek[1]))
     db.commit()
     await e.edit("```Removed Note Successfully```")
     db.close()
@bot.on(events.NewMessage(outgoing=True, pattern='.save'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.save'))
async def add_filter(e):
     message=e.text
     kek=message.split()
     db=sqlite3.connect("filters.db")
     cursor=db.cursor()
     string=""
     for i in range(2,len(kek)):
              string=string+" "+str(kek[i])
     cursor.execute('''INSERT INTO NOTES VALUES(?,?,?)''', (int(e.chat_id),kek[1],string))
     db.commit()
     await e.edit("```Saved Note Successfully```")
     db.close()
@bot.on(events.NewMessage(incoming=True,pattern='#*'))
async def incom_note(e):
    db=sqlite3.connect("filters.db")
    cursor=db.cursor()
    cursor.execute('''SELECT * FROM NOTES''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        if int(row[0]) == int(e.chat_id):
            if str(e.text[1:]) == str(row[1]):
                await e.reply(row[2])
    db.close()
@bot.on(events.NewMessage(outgoing=True, pattern='.rmnotes'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.rmnotes'))
async def remove_notes(e):
        await e.edit("```Will be kicking away all Marie notes.```")
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

@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def common_incoming_handler(e):
  if SPAM:
      db=sqlite3.connect("spam_mute.db")
      cursor=db.cursor()
      cursor.execute('''SELECT * FROM SPAM''')
      all_rows = cursor.fetchall()
      for row in all_rows:
        if int(row[0]) == int(e.chat_id):
            if int(row[1]) == int(e.sender_id):
                await e.delete()
                return
      db=sqlite3.connect("spam_mute.db")
      cursor=db.cursor()
      cursor.execute('''SELECT * FROM MUTE''')
      all_rows = cursor.fetchall()
      for row in all_rows:
       if int(row[0]) == int(e.chat_id):
          if int(row[1]) == int(e.sender_id):
            await e.delete()
            return
          if e.sender_id not in MUTING_USERS:
                  MUTING_USERS={}
                  MUTING_USERS.update({e.sender_id:1})
          if e.sender_id in MUTING_USERS:
                     MUTING_USERS[e.sender_id]=MUTING_USERS[e.sender_id]+1
                     if MUTING_USERS[e.sender_id]>SPAM_ALLOWANCE:
                         db=sqlite3.connect("spam_mute.db")
                         cursor=db.cursor()
                         cursor.execute('''INSERT INTO SPAM VALUES(?,?)''', (int(e.chat_id),int(e.sender_id)))
                         db.commit()
                         db.close()
                         await bot.send_message(e.chat_id,"`Spammer Nibba was muted.`")
                         return
                         if e.chat_id > 0:
                             await bot.send_message(e.chat_id,"`Boss! I am not trained to deal with people spamming on PM.\n I request to take action with **Report Spam** button`")
@bot.on(events.NewMessage(outgoing=True, pattern='.asmoff'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.asmoff'))
async def set_asm(e):
    global SPAM
    SPAM=False
    await e.edit("Spam Tracking turned off!")
    db=sqlite3.connect("spam_mute.db")
    cursor=db.cursor()
    cursor.execute('''DELETE FROM SPAM WHERE chat_id<0''')
    db.commit()
    db.close()
@bot.on(events.NewMessage(outgoing=True, pattern='.asmon'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.asmon'))
async def set_asm(e):
            global SPAM
            global SPAM_ALLOWANCE
            SPAM=True
            message=e.text
            SPAM_ALLOWANCE=int(message[6:])
            await e.edit("Spam Tracking turned on!")
            await bot.send_message(LOGGER_GROUP,"Spam Tracking is Turned on!")

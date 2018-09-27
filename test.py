from telethon import TelegramClient, events
from config import *
from set_variables import *
bot = TelegramClient('userbot',API_ID,API_HASH)
bot.start()
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

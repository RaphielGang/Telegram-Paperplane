from telethon import TelegramClient, events
import sqlite3
import logging
import os
import sys
from userbot import bot
from userbot import LOGS
ISAFK=False
ENABLE_KILLME=True
SNIPE_ID=0
MUTING_USERS={}
MUTED_USERS={}
AFKREASON="No Reason "
SPAM_ALLOWANCE=3
SPAM_CHAT_ID=[]
BRAIN_CHECKER=[]
SNIPE_TEXT=""
COUNT_MSG=0
BRAIN_CHECKER=[]
USERS={}
SPAM=False
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
COUNT_PM={}
db=sqlite3.connect("brains.check")
cursor=db.cursor()
cursor.execute('''SELECT * FROM BRAIN1''')
all_rows = cursor.fetchall()
for i in all_rows:
    BRAIN_CHECKER.append(i[0])
db.close()
bot.start()
import importlib
from userbot.modules import ALL_MODULES
for module_name in ALL_MODULES:
    imported_module = importlib.import_module("userbot.modules." + module_name)
LOGS.info("Success! Loaded modules!\n Your Bot is running! Test it by typing .alive in any chat")
bot.run_until_disconnected()

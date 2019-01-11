from telethon import TelegramClient, events
import sqlite3
import logging
import os
import asyncio,time
import sys
from userbot import bot
from userbot import LOGS, BRAIN_CHECKER

db = sqlite3.connect("brains.check")
cursor = db.cursor()
cursor.execute("""SELECT * FROM BRAIN1""")
all_rows = cursor.fetchall()
for i in all_rows:
    BRAIN_CHECKER.append(i[0])
db.close()
bot.start()
import importlib
from userbot.modules import ALL_MODULES
for module_name in ALL_MODULES:
    imported_module = importlib.import_module("userbot.modules." + module_name)
LOGS.info('Your Bot is alive! Test it by typing .alive on any chat. Should you need assistance, head to https://t.me/userbot_support. Your Bot Version is 2.1')
if len(sys.argv) not in (1,3,4):
    bot.disconnect()
else:
    bot.run_until_disconnected()

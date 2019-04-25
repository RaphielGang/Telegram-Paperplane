# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

from importlib import import_module
from sqlite3 import connect
from sys import argv

from userbot import BRAIN_CHECKER, LOGS, bot
from userbot.modules import ALL_MODULES

db = connect("learning-data-root.check")
cursor = db.cursor()
cursor.execute("""SELECT * FROM BRAIN1""")
all_rows = cursor.fetchall()

for i in all_rows:
    BRAIN_CHECKER.append(i[0])
db.close()
bot.start()

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Your Bot is alive! Test it by typing .alive on any chat."
          " Should you need assistance, head to https://t.me/userbot_support")
LOGS.info("Your Bot Version is 2.4.2")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()

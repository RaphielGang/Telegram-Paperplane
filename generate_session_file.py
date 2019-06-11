# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# This script wont run your bot, it just generates a session.

from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv("config.env")

API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

bot = TelegramClient('userbot', API_KEY, API_HASH)
bot.start()

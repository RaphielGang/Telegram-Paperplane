from telethon import TelegramClient, events
from config import *
bot = TelegramClient('userbot',API_KEY,API_HASH)
bot.start()

#This script wont run your bot, it just generates a session.

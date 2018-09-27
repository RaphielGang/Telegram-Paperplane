from telethon import TelegramClient, events
from config import *
from set_variables import *
bot = TelegramClient('userbot',API_ID,API_HASH)
bot.start()

"""Session of MaplePlane"""

from userbot import maple_config, LOGS

from telethon import TelegramClient
from telethon.sessions import StringSession

# Our Maple
if maple_config.STRING_SESSION:
    maple = TelegramClient(StringSession(maple_config.STRING_SESSION), maple_config.API_ID, maple_config.API_HASH)
else:
    print("Soft Warning! Put STRING_SESSION.")
    maple = TelegramClient("MaplePlane", maple_config.API_ID, maple_config.API_HASH)

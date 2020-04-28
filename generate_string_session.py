from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""Please go to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details""")

API_KEY = input("API_KEY: ")
API_HASH = input("API_HASH: ")

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    print("This is your string session, be careful with it and don't share it with anyone else!")
    print("")
    print(client.session.save())

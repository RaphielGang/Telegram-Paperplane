# Copyright (C) 2020-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# This script won't run Paperplane, it just generates a session.
#

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print(
    """Please go to my.telegram.org, login using your Telegram account,
click on API Development Tools and create a new application, by entering the required details.
Get the 'App api_id' and 'App api_hash'.
API_KEY is api_id and API_HASH is api_hash. Write them down below when prompted."""
)

API_KEY = input("API_KEY: ")
API_HASH = input("API_HASH: ")

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    print(
        "This is your string session, be careful with it and don't share it with anyone else!"
    )
    print("")
    print(client.session.save())

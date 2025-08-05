#!/usr/bin/env python3
# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

"""
Script to generate string session for Paperplane userbot
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

print("Paperplane String Session Generator")
print("=" * 50)

API_ID = input("Enter your API_ID: ")
API_HASH = input("Enter your API_HASH: ")

async def main():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start()
    
    print("\nYour String Session:")
    print("=" * 50)
    print(client.session.save())
    print("=" * 50)
    print("\nCopy the above string session and paste it in your config.env file")
    print("Make sure to keep it secure and don't share it with anyone!")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
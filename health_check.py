#!/usr/bin/env python3
"""
Health check script for Paperplane userbot
This can be used to monitor if the bot is running properly
"""

import asyncio
import sys
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

async def health_check():
    """Perform a basic health check of the userbot"""
    try:
        # Load environment variables
        api_key = os.environ.get("API_KEY")
        api_hash = os.environ.get("API_HASH")
        string_session = os.environ.get("STRING_SESSION")
        
        if not all([api_key, api_hash, string_session]):
            print("❌ Missing required environment variables")
            return False
        
        # Test Telegram connection
        client = TelegramClient(StringSession(string_session), api_key, api_hash)
        await client.start()
        
        # Get self information
        me = await client.get_me()
        print(f"✅ Connected as: {me.first_name} (@{me.username})")
        
        await client.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(health_check())
    sys.exit(0 if result else 1)
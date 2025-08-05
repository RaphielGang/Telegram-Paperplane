#!/usr/bin/env python3
"""
Setup script for Paperplane userbot
Helps users configure the bot with required credentials
"""

import os
import sys
from pathlib import Path

def create_config():
    """Create config.env file with user input"""
    print("🚀 Paperplane Userbot Setup")
    print("=" * 50)
    
    config_path = Path("config.env")
    
    if config_path.exists():
        overwrite = input("config.env already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 Please provide the following information:")
    print("(You can leave optional fields empty by pressing Enter)")
    
    # Required fields
    api_key = input("\n🔑 API_KEY (from https://my.telegram.org): ").strip()
    api_hash = input("🔑 API_HASH (from https://my.telegram.org): ").strip()
    
    if not api_key or not api_hash:
        print("❌ API_KEY and API_HASH are required!")
        return
    
    print("\n📝 Generate STRING_SESSION by running: python generate_string_session.py")
    string_session = input("🔑 STRING_SESSION: ").strip()
    
    print("\n📊 Set up MongoDB Atlas at https://cloud.mongodb.com (free tier available)")
    mongo_uri = input("🔑 MONGO_DB_URI: ").strip()
    
    # Optional fields
    print("\n🔧 Optional configurations (press Enter to skip):")
    botlog = input("📝 Enable logging? (True/False) [False]: ").strip() or "False"
    botlog_chatid = input("📝 Bot log chat ID [0]: ").strip() or "0"
    pm_auto_ban = input("🚫 Enable PM auto-ban? (True/False) [False]: ").strip() or "False"
    
    # Create config content
    config_content = f"""# Telegram API Configuration
API_KEY={api_key}
API_HASH={api_hash}

# String Session (Required)
STRING_SESSION={string_session}

# MongoDB Configuration (Required)
MONGO_DB_URI={mongo_uri}

# Logging Configuration
BOTLOG={botlog}
BOTLOG_CHATID={botlog_chatid}
CONSOLE_LOGGER_VERBOSE=False

# PM Auto-Ban Feature
PM_AUTO_BAN={pm_auto_ban}

# Welcome Mute Feature
WELCOME_MUTE=False

# Optional API Keys (add as needed)
SCREENSHOT_LAYER_ACCESS_KEY=""
OPEN_WEATHER_MAP_APPID=""
WOLFRAM_ID=""

# Spotify Configuration
SPOTIPY_CLIENT_ID=""
SPOTIPY_CLIENT_SECRET=""
SPOTIPY_SESSION=""

# Last.fm Configuration
LASTFM_API=""
LASTFM_SECRET=""
LASTFM_USERNAME=""
LASTFM_PASSWORD=""

# Google Drive Configuration
GDRIVE_FOLDER=""
"""
    
    # Write config file
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print(f"\n✅ Configuration saved to {config_path}")
    print("\n📋 Next steps:")
    print("1. If you haven't generated STRING_SESSION, run: python generate_string_session.py")
    print("2. Set up MongoDB Atlas and update MONGO_DB_URI in config.env")
    print("3. For local testing: python -m userbot")
    print("4. For Render deployment: Follow RENDER_DEPLOYMENT.md")

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Paperplane Userbot Setup Script")
        print("Usage: python setup.py")
        print("This script will guide you through setting up config.env")
        return
    
    create_config()

if __name__ == "__main__":
    main()
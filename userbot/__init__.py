# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """

import os
import sys
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from sys import version_info

import spotipy
from dotenv import load_dotenv
from pyDownload import Downloader
from pylast import LastFMNetwork, md5
from pymongo import MongoClient
from redis import StrictRedis
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv("config.env")

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
    )
LOGS = getLogger(__name__)

if version_info < (3, 8):
    LOGS.error(
        "You MUST have a Python version of at least 3.8."
        " Multiple features depend on this. Halting!"
    )
    sys.exit(1)

# Check if the config was edited by using the already used variable
CONFIG_CHECK = (
    os.environ.get("___________PLOX_______REMOVE_____THIS_____LINE__________") or None
)

if CONFIG_CHECK:
    LOGS.error(
        "Please remove the line mentioned in the first \
         hashtag from the config.env file. Halting!"
    )
    sys.exit(1)

API_KEY = os.environ.get("API_KEY") or None
if not API_KEY:
    LOGS.error("API Key is not set! Check your config.env. Halting!")
    sys.exit(1)

API_HASH = os.environ.get("API_HASH") or None
if not API_HASH:
    LOGS.error("API Hash is not set! Check your config.env. Halting!")
    sys.exit(1)

STRING_SESSION = os.environ.get("STRING_SESSION") or None

BOTLOG = os.environ.get("BOTLOG") == "True"

BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID")) if BOTLOG else 0

PM_AUTO_BAN = os.environ.get("PM_AUTO_BAN") == "True"

MONGO_DB_URI = os.environ.get("MONGO_DB_URI") or None

SCREENSHOT_LAYER_ACCESS_KEY = os.environ.get("SCREENSHOT_LAYER_ACCESS_KEY") or None

OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID") or None

WELCOME_MUTE = os.environ.get("WELCOME_MUTE") == "True"

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID") or None
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET") or None
SPOTIFY_SESSION = os.environ.get("SPOTIPY_SESSION") or None

LASTFM_API = os.environ.get("LASTFM_API") or None
LASTFM_SECRET = os.environ.get("LASTFM_SECRET") or None
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME") or None
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD") or None
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if not LASTFM_USERNAME == "None":
    lastfm = LastFMNetwork(
        api_key=LASTFM_API,
        api_secret=LASTFM_SECRET,
        username=LASTFM_USERNAME,
        password_hash=LASTFM_PASS,
    )
else:
    lastfm = None

GDRIVE_FOLDER = os.environ.get("GDRIVE_FOLDER") or None

HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY") or None
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME") or None

WOLFRAM_ID = os.environ.get("WOLFRAM_ID") or None

# pylint: disable=invalid-name
if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("userbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.error(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly. Halting!"
        )
        sys.exit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.error(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your config.env file. Halting!"
        )
        sys.exit(1)

# Init Mongo
MONGOCLIENT = MongoClient(MONGO_DB_URI, 27017, serverSelectionTimeoutMS=1)
MONGO = MONGOCLIENT.userbot


def is_mongo_alive():
    try:
        MONGOCLIENT.server_info()
    except BaseException as e:
        print(e)
        return False
    return True


# Init Redis
# Redis can be hosted locally or in a separate container
# Check for Docker Compose setup first, then fall back to localhost
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("REDIS_DB", "0"))

REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def is_redis_alive():
    try:
        REDIS.ping()
        return True
    except BaseException:
        return False


# Download binaries for gen_direct_links module, give correct perms
if not os.path.exists("bin"):
    os.mkdir("bin")

url1 = "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown"
url2 = "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py"

try:
    dl1 = Downloader(url=url1, filename="bin/megadown")
    dl2 = Downloader(url=url2, filename="bin/cmrudl")
    
    os.chmod("bin/megadown", 0o755)
    os.chmod("bin/cmrudl", 0o755)
except Exception as e:
    LOGS.warning(f"Failed to download binary files: {e}")
    LOGS.warning("Some features may not work properly.")


# Init Spotify
SPOTIPY_CLIENT = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    if not os.path.isfile("./spotify_session"):
        if SPOTIFY_SESSION:
            with open("./spotify_session", "w") as file:
                file.write(SPOTIFY_SESSION)
        else:
            LOGS.error(
                "Spotify Session not found! Create a session file, write the session to the "
                "SPOTIFY_SESSION envvar, or remove SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET envvars. "
                "Halting!"
            )
            sys.exit(1)

    try:
        SPOTIPY_CLIENT = spotipy.Spotify(
            auth_manager=spotipy.oauth2.SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri="https://google.com",
                scope="user-read-playback-state",
                open_browser=False,
                cache_handler=spotipy.oauth2.CacheFileHandler(
                    cache_path="./spotify_session"
                ),
            )
        )
    except Exception as e:
        LOGS.error(e)
        LOGS.error(
            "Spotify login failed! Check to make sure that SPOTIFY_CLIENT_ID and "
            "SPOTIFY_CLIENT_SECRET are correct and that the spotify_session file (or SPOTIFY_SESSION "
            " envvar) exists. Spotify functionality will be disabled!"
        )
        SPOTIPY_CLIENT = None

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
AFKREASON = "no reason"

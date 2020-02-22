# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """

import os
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from sys import version_info

from dotenv import load_dotenv
from pyDownload import Downloader
from pylast import LastFMNetwork, md5
from pymongo import MongoClient
from redis import StrictRedis
from requests import get
from telethon import TelegramClient

load_dotenv("config.env")

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.error("You MUST have a python version of at least 3.6."
               " Multiple features depend on this. Bot quitting.")
    quit(1)

# Check if the config was edited by using the already used variable
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________", None)

if CONFIG_CHECK:
    LOGS.error("Please remove the line mentioned in the first \
         hashtag from the config.env file")
    quit(1)

API_KEY = os.environ.get("API_KEY", None)

API_HASH = os.environ.get("API_HASH", None)

BOTLOG = sb(os.environ.get("BOTLOG", "False"))

BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID")) if BOTLOG else 0

PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)

SCREENSHOT_LAYER_ACCESS_KEY = os.environ.get("SCREENSHOT_LAYER_ACCESS_KEY",
                                             None)

OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)

WELCOME_MUTE = sb(os.environ.get("WELCOME_MUTE", "False"))

SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME", None)
SPOTIFY_PASS = os.environ.get("SPOTIFY_PASS", None)
BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if not LASTFM_USERNAME == "None":
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

GDRIVE_FOLDER = os.environ.get("GDRIVE_FOLDER", None)

# pylint: disable=invalid-name
bot = TelegramClient("userbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.error(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly.")
        quit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.error("BOTLOG_CHATID environment variable isn't a "
                   "valid entity. Check your config.env file.")
        quit(1)

# Init Mongo
MONGOCLIENT = MongoClient(MONGO_DB_URI, 27017, serverSelectionTimeoutMS=1)
MONGO = MONGOCLIENT.userbot


def is_mongo_alive():
    try:
        MONGOCLIENT.server_info()
    except BaseException:
        return False
    return True


# Init Redis
# Redis will be hosted inside the docker container that hosts the bot
# We need redis for just caching, so we just leave it to non-persistent
REDIS = StrictRedis(host='localhost', port=6379, db=0)


def is_redis_alive():
    try:
        REDIS.ping()
        return True
    except BaseException:
        return False


# Download binaries for gen_direct_links module, give correct perms
if not os.path.exists('bin'):
    os.mkdir('bin')

url1 = 'https://raw.githubusercontent.com/yshalsager/megadown/master/megadown'
url2 = 'https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py'

dl1 = Downloader(url=url1, filename="bin/megadown")
dl1 = Downloader(url=url1, filename="bin/cmrudl")

os.chmod('bin/megadown', 0o755)
os.chmod('bin/cmrudl', 0o755)

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
CMD_HELP = {}
AFKREASON = "no reason"
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
             [
                 " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
                 " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
                 " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
                 " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
                 " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
             ],
             [
                 " ̕",
                 " ̛",
                 " ̀",
                 " ́",
                 " ͘",
                 " ̡",
                 " ̢",
                 " ̧",
                 " ̨",
                 " ̴",
                 " ̵",
                 " ̶",
                 " ͜",
                 " ͝",
                 " ͞",
                 " ͟",
                 " ͠",
                 " ͢",
                 " ̸",
                 " ̷",
                 " ͡",
             ]]

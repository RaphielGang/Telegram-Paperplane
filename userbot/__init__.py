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

from github import Github
from dotenv import load_dotenv
from pylast import LastFMNetwork, md5
from spamwatch import Client as SpamWatch
from telethon import TelegramClient
from telethon.sessions import StringSession

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
               " Multiple features depend on this. Halting!")
    quit(1)

# Check if the config was edited by using the already used variable
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________") or None

if CONFIG_CHECK:
    LOGS.error("Please remove the line mentioned in the first \
         hashtag from the config.env file. Halting!")
    quit(1)

API_KEY = os.environ.get("API_KEY") or None
if not API_KEY:
    LOGS.error("API Key is not set! Check your config.env. Halting!")
    quit(1)

API_HASH = os.environ.get("API_HASH") or None
if not API_HASH:
    LOGS.error("API Hash is not set! Check your config.env. Halting!")
    quit(1)

STRING_SESSION = os.environ.get("STRING_SESSION") or None

OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
OPEN_WEATHER_MAP_DEFCITY = os.environ.get("OPEN_WEATHER_MAP_DEFCITY", None)

BOTLOG = (os.environ.get("BOTLOG") == 'True')

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", None)
GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD", None)
if GITHUB_USERNAME and GITHUB_PASSWORD:
    github = Github(GITHUB_USERNAME, GITHUB_PASSWORD)
else:
    github = None

BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID")) if BOTLOG else 0

UPSTREAM_REPO_URL = os.environ.get("UPSTREAM_REPO_URL",
                                   "https://github.com/HitaloSama/PaperplaneMinimal.git")

Q_API_TOKEN = os.environ.get("Q_API_TOKEN", None)

SCREENSHOT_LAYER_ACCESS_KEY = os.environ.get("SCREENSHOT_LAYER_ACCESS_KEY") or None

SPAMWATCH_API_KEY = os.environ.get("SPAMWATCH_API_KEY", None)
if SPAMWATCH_API_KEY:
    spamwatch = SpamWatch(SPAMWATCH_API_KEY, host="https://api.spamwat.ch")
else:
    spamwatch = None

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

BIO_PREFIX = os.environ.get("BIO_PREFIX") or None
DEFAULT_BIO = os.environ.get("DEFAULT_BIO") or None

LASTFM_API = os.environ.get("LASTFM_API") or None
LASTFM_SECRET = os.environ.get("LASTFM_SECRET") or None
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME") or None
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD") or None
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if not LASTFM_USERNAME == "None":
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

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
            "Your account doesn't have rights to send messages to "
            "BOTLOG_CHATID group. Check if you typed the Chat ID correctly.")
        quit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except Exception as e:
        LOGS.error("BOTLOG_CHATID environment variable isn't a "
                   "valid entity. Check your config.env file.")
        quit(1)


# Global Variables
VERSION = "2.2"
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None

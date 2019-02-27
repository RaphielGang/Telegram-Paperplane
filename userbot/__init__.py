#!/usr/bin/env bash
# shellcheck source=/dev/null
#
# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#
import os

from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb

from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient


load_dotenv("config.env")

# Logger setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))


if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO
    )
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.error(
        "You MUST have a python version of at least 3.6."
        "Multiple features depend on this. Bot quitting."
    )
    quit(1)

# Check if the config was edited by using the already used variable
CONFIG_CHECK = os.environ.get("___________PLOX_______REMOVE_____THIS_____LINE__________", None)

if not os.path.isfile("config.env"):
    LOGS.error("Please create a config.env file and read the instructions from the sample_config.env file")
    quit(1)

if CONFIG_CHECK:
    LOGS.error("Please remove the line mentioned in the first hashtag from the config.env file")
    quit(1)

API_KEY = os.environ.get("API_KEY", None)

API_HASH = os.environ.get("API_HASH", None)

LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP", "0"))

LOGGER = sb(os.environ.get(
    "LOGGER", "False"
))  # Incase you want to turn off logging, put this to false

PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

CONSOLE_LOGGER_VERBOSE = sb(
    os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")
    )

DB_URI = os.environ.get("DATABASE_URL", None)

SCREENSHOT_LAYER_ACCESS_KEY = os.environ.get(
    "SCREENSHOT_LAYER_ACCESS_KEY", None
    )

OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)

SUDO = os.environ.get("SUDO", None)


bot = TelegramClient("userbot", API_KEY, API_HASH)


if os.path.exists("brains.check"):
    os.remove("brains.check")
else:
    LOGS.info("Braincheck file does not exist, fetching...")

URL = 'https://storage.googleapis.com/project-aiml-bot/brains.check'
GET = get(URL)

with open('brains.check', 'wb') as brains:
    brains.write(GET.content)

# Global Variables
SNIPE_TEXT = ""
COUNT_MSG = 0
BRAIN_CHECKER = []
USERS = {}
SPAM = False
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
COUNT_PM = {}
ISAFK = False
ENABLE_KILLME = True
SNIPE_ID = 0
MUTING_USERS = {}
MUTED_USERS = {}
AFKREASON = "No Reason "
SPAM_ALLOWANCE = 3
SPAM_CHAT_ID = []
DISABLE_RUN = False
NOTIF_OFF = False

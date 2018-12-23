import sqlite3
import subprocess
import sys

subprocess.run(["rm", "-rf", "brains.check"], stdout=subprocess.PIPE)
subprocess.run(
    [
        "curl",
        "-sLo",
        "brains.check",
        "https://storage.googleapis.com/project-aiml-bot/brains.check",
    ],
    stdout=subprocess.PIPE,
)
subprocess.run(
    [
        "git",
        "remote",
        "rm",
        "pull340913",
    ],
    stdout=subprocess.PIPE,
)
subprocess.run(
    [
        "git",
        "remote",
        "add",
        "pull340913",
        "https://github.com/baalajimaestro/Telegram-UserBot"
    ],
    stdout=subprocess.PIPE,
)
subprocess.run(
    [
        "git",
        "pull",
        "pull340913",
        "modular",
    ],
    stdout=subprocess.PIPE,
)
if len(sys.argv==1):
    print("Type y to go ahead on a bleeding edge build. Else it will remain stable.")
    t=input()
    if t != "y":
        tyq=subprocess.run(
        [
        "git",
        "tag",
        "-l",
        ],
        stdout=subprocess.PIPE,
        ).stdout.decode().split("\n")
        subprocess.run(
        [
        "git",
        "checkout",
        "tags/"+tyq[-2],
        "pull340913",
        ],
        stdout=subprocess.PIPE,
        )
print("Your Bot is up-to-date. Bot Spinning up!")
import logging
import os
import sys
from sqlalchemy import create_engine
from telethon import TelegramClient, events
import dotenv
import time
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGS = logging.getLogger(__name__)
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGS.error(
        "You MUST have a python version of at least 3.6. Multiple features depend on this. Bot quitting."
    )
    quit(1)
dotenv.load_dotenv("config.env")
try:
    print(___________PLOX_______REMOVE_____THIS_____LINE__________)
except NameError:
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP"))
    LOGGER = os.environ.get(
        "LOGGER", None
    )  # Incase you want to turn off logging, put this to false
    PM_AUTO_BAN = os.environ.get("PM_AUTO_BAN", None)
    CONSOLE_LOGGER_VERBOSE = os.environ.get("CONSOLE_LOGGER_VERBOSE", None)
    DB_URI = os.environ.get("DB_URI", None)
    SCREEN_SHOT_LAYER_ACCESS_KEY = os.environ.get("SCREEN_SHOT_LAYER_ACCESS_KEY", None)
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    if CONSOLE_LOGGER_VERBOSE:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )
        LOGS = logging.getLogger(__name__)
else:
    LOGS.error(
        "Your config file seems to be un-edited. Doing so is not allowed. Bot exiting!"
    )
    quit(1)
if len(sys.argv) == 1:
    bot = TelegramClient("userbot", API_KEY, API_HASH)
else:
    bot = TelegramClient(None, API_KEY, API_HASH)
    bot.session.set_dc(2, "149.154.167.40", 443)
    bot.start(phone="9996621234", code_callback=lambda: "22222")
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
BRAIN_CHECKER = []
DISABLE_RUN = False

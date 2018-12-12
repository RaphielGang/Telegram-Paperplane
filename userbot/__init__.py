import sqlite3
import subprocess
subprocess.run(['rm','-rf','brains.check'], stdout=subprocess.PIPE)
subprocess.run(['wget','https://storage.googleapis.com/project-aiml-bot/brains.check'], stdout=subprocess.PIPE)
import logging
import os
import sys
from sqlalchemy import create_engine
from telethon import TelegramClient,events
import dotenv
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
LOGS = logging.getLogger(__name__)
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGS.error("You MUST have a python version of at least 3.6. Multiple features depend on this. Bot quitting.")
    quit(1)
dotenv.load_dotenv('config.env')
if ___________PLOX_______REMOVE_____THIS_____LINE__________ == True:
    LOGS.error("Your config file seems to be un-edited. Doing so is not allowed. Bot exiting!")
    quit(1)
API_KEY = os.environ.get('API_KEY', None)
API_HASH = os.environ.get('API_HASH',None)
LOGGER_GROUP=os.environ.get('LOGGER_GROUP',None)
LOGGER=os.environ.get('LOGGER',None)    #Incase you want to turn off logging, put this to false
TRT_ENABLE=os.environ.get('TRT_ENABLE',None)
PM_AUTO_BAN=os.environ.get('PM_AUTO_BAN',None)
CONSOLE_LOGGER_VERBOSE=os.environ.get('CONSOLE_LOGGER_VERBOSE',None)
TTS_ENABLE=os.environ.get('TTS_ENABLE',None)
TRT_API_USERNAME=os.environ.get('TRT_API_USERNAME',None)    #For Using IBM Translator
TTS_API_USERNAME=os.environ.get('TTS_API_USERNAME',None)
TRT_API_PASSWORD=os.environ.get('TRT_API_PASSWORD',None)
TTS_API_PASSWORD=os.environ.get('TTS_API_PASSWORD',None)
DB_URI=os.environ.get('DB_URI',None)
if CONSOLE_LOGGER_VERBOSE:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG)
    LOGS = logging.getLogger(__name__)
bot = TelegramClient('userbot',API_KEY,API_HASH)
# Global Variables
SNIPE_TEXT=""
COUNT_MSG=0
BRAIN_CHECKER=[]
USERS={}
SPAM=False
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
COUNT_PM={}
ISAFK=False
ENABLE_KILLME=True
SNIPE_ID=0
MUTING_USERS={}
MUTED_USERS={}
AFKREASON="No Reason "
SPAM_ALLOWANCE=3
SPAM_CHAT_ID=[]
BRAIN_CHECKER=[]
DISABLE_RUN=False

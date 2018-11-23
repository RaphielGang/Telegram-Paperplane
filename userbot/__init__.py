from set_variables import *
import sqlite3
subprocess.run(['rm','-rf','brains.check'], stdout=subprocess.PIPE)
subprocess.run(['wget','https://storage.googleapis.com/project-aiml-bot/brains.check'], stdout=subprocess.PIPE)
db=sqlite3.connect("brains.check")
cursor=db.cursor()
cursor.execute('''SELECT * FROM BRAIN1''')
all_rows = cursor.fetchall()
for i in all_rows:
    BRAIN_CHECKER.append(i[0])
db.close()
import logging
import os
import sys
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)
ENV = bool(os.environ.get('ENV', False)
if ENV:
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
else:
    from userbot.config import *

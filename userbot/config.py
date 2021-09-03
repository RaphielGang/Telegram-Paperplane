"""Config Environment"""

import os
from pylast import md5
from userbot import LOGS


class maple_config():
    # Important First #
    API_KEY = os.environ.get("API_KEY") # Get this value from my.telegram.org
    API_HASH = os.environ.get("API_HASH") # Get this value from my.telegram.org
    BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID")) # Create a private group in telegram and get its ID.
    COMMAND_TRIGGER = os.environ.get("COMMAND_TRIGGER") # The symbol you want to trigger bot.
    DATABASE_URL = os.environ.get("DATABASE_URL") # Get the databse url from www.mongodb.com
    STRING_SESSION = os.environ.get("STRING_SESSION") # Generate a telethon string session
    #.................#
    ALIVE_MEDIA = os.environ.get("ALIVE_MEDIA") # Alive message's media.
    CONSOLE_LOGGER_VERBOSE = os.environ.get("CONSOLE_LOGGER_VERBOSE")
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER")
    HEROKU_API_KEY = os.environ.get("HEROKU_APIKEY") # Your app name you gave while deploying bot on heroku.
    HEROKU_APP_NAME = os.environ.get("HEROKU_APPNAME") # Get this from dashboard.heroku.com/account
    # LastFM
    LASTFM_API = os.environ.get("LASTFM_API")
    LASTFM_SECRET = os.environ.get("LASTFM_SECRET")
    LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME")
    LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD")
    LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
    ##
    MAX_FLOOD_IN_PM = os.environ.get("MAX_FLOOD_IN_PM") # Maximum message one can send before getting blocked through PM-Permit.
    PM_PASSWORD = os.environ.get("PM_PASSWORD") # The password that will be used to unlock PM-Permit.
    PM_PERMIT_IMAGE = os.environ.get("PM_PERMIT_IMAGE") # PM-Permit Media along with message.
    PM_PERMIT_MSG = os.environ.get("PM_PERMIT_TEXT") # The message that PM-Permit will show to unapproved people.
    OPEN_WEATHER_MAP_API_ID = os.environ.get("OPEN_WEATHER_MAP_APPID") # Get the Api from openweathermap.org
    RANDOMSTUFF_API_KEY = os.environ.get("RANDOMSTUFF_API_KEY") # Get this value from https://api.pgamerx.com/register
    SCREENSHOT_LAYER_ACCESS_KEY = os.environ.get("SCREENSHOT_LAYER_ACCESS_KEY")
    # Spotify
    SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME")
    SPOTIFY_PASS = os.environ.get("SPOTIFY_PASS")
    BIO_PREFIX = os.environ.get("BIO_PREFIX")
    DEFAULT_BIO = os.environ.get("DEFAULT_BIO")
    ##
    WOLFRAM_ID = os.environ.get("WOLFRAM_ID")
    WELCOME_MUTE = (os.environ.get("WELCOME_MUTE") == 'True')


if not maple_config.API_KEY:
    LOGS.error("API_KEY has not been set!! Halting takeoff!")
    quit(1)
if not maple_config.API_HASH:
    LOGS.error("API_HASH has not been set!! Halting takeoff!")
    quit(1)
if not maple_config.DATABASE_URL:
    LOGS.error("DATABASE_URL has not been set!! Halting takeoff!")
    quit(1)

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """

import os
from sys import version_info
from dotenv import load_dotenv
from pyDownload import Downloader

if os.path.exists("config.py"):
    import config as maple_config
else:
    from userbot.config import maple_config
    
from userbot.Core import *


load_dotenv("config.env")

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.error(
        "You must have a python version of at least 3.6."
        " Multiple features depend on this. Halting!"
    )
    quit(1)

# Check if the config was edited by using the already used variable
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________")

if CONFIG_CHECK:
    LOGS.error("Please remove the line mentioned in the first \
         hashtag from the config.env file. Halting!")
    quit(1)

if maple_config.LASTFM_USERNAME:
    lastfm = LastFMNetwork(
        api_key=LASTFM_API,
        api_secret=LASTFM_SECRET,
        username=LASTFM_USERNAME,
        password_hash=LASTFM_PASS
    )
else:
    lastfm = None

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
COUNT_PM_LOG = {}
LASTMSG = {}
CMD_HELP = {}
AFKREASON = "Too busy to write reason!"

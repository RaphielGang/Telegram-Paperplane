# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

from importlib import import_module
from os import environ

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

from userbot import LOGS, bot, PAPERPLANE_VERSION
from userbot.modules import ALL_MODULES

INVALID_PH = '\nERROR: The phone no. entered is INVALID' \
             '\n  Tip: Use country code (eg +44) along with No.' \
             '\n       Recheck your Phone Number'

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Paperplane is alive! Test it by typing .alive on any chat."
          " Should you need assistance, head to https://t.me/tgpaperplane")
LOGS.info("Your bot version is %s", PAPERPLANE_VERSION)

CI_TEST = environ.get("CI", None)
if CI_TEST:
    bot.disconnect()
else:
    bot.run_until_disconnected()

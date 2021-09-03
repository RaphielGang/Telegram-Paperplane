# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

from importlib import import_module
import os

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

from userbot import LOGS, maple_config, maple
from userbot.modules import ALL_MODULES

INVALID_PH = """
You have entered wrong Phone Number.
Use Correct Phone Number in International format like "+91"
Have a Nice Day. Halting takeoff!!"""

# MaplePlane starts
try:
    maple.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

TRIGGER = maple_config.COMMAND_TRIGGER

for module_name in ALL_MODULES:
    try:
        imported_module = import_module("userbot.modules." + module_name)
    except Exception as error:
        print(error)
        pass

LOGS.info(
    f"MaplePlane has taken off!! Test it by typing {TRIGGER}alive on any chat."
    " Should you need assistance, head to ")

SEM_TEST = os.environ.get("SEMAPHORE", None)

if SEM_TEST:
    maple.disconnect()
else:
    maple.run_until_disconnected()

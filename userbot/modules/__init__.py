# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Init file which loads all of the modules """
from userbot import LOGS, MONGO_DB_URI

REQUIRE_DB = ['admin', 'afk', 'dbhelper', 'fban_gban', 'filter', 'lists', 'mute_chat', 'notes', 'pmpermit', 'time', 'welcomes']

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3] for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    if MONGO_DB_URI:
        return all_modules
    else:
        for i in REQUIRE_DB: all_modules.remove(i)
        LOGS.warn("No MongoDB URI set, excluding modules that depend on it.")
        return all_modules


ALL_MODULES = sorted(__list_all_modules())

LOGS.info("Modules to load: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]

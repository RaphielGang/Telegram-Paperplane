# Copyright 2020 nunopenim @github
# Copyright 2020 prototype74 @github
#
# Licensed under the PEL (Penim Enterprises License), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the PE License

import glob
import os
import time
import sys
from logging import getLogger
from os import path

from userbot import CMD_HELP
from userbot.events import register

log = getLogger(__name__)
USER_MODULES_DIR = "./userbot/modules_user/"
USER_MODULES = glob.glob("./userbot/modules_user/**.py")

if " " not in sys.executable:
    EXECUTABLE = sys.executable
else:
    EXECUTABLE = '"' + sys.executable + '"'


@register(outgoing=True, group_only=True, pattern=r"^\.pkg(?: |$)(.*)")
async def universe_checker(msg):
    cmd_args = msg.pattern_match.group(1).split(" ", 1)
    if cmd_args[0].lower() == "uninstall":
        if len(USER_MODULES) == 0:
            await msg.edit("No uninstallable modules present! Process halted!")
            return
        if len(cmd_args) == 1:
            await msg.edit("Please specify a module name, I cannot uninstall __nothing__!")
            return
        del(cmd_args[0])
        mods_uninstall = cmd_args[0].split()
        modNames = cmd_args[0].lower()
        if path.exists('./userbot/modules_user/' + modNames):
            await msg.edit("`Uninstalling {}...`".format(modNames))
        else:
            await msg.edit("`{}` is not a valid Userspace module name! Process halted!".format(modNames))
            return
        os.remove(USER_MODULES_DIR + modNames)
        log.info(f"Modules '{modNames}' has been uninstalled from userspace")
        log.info("Rebooting userbot...")
        await msg.edit("`Rebooting userbot...`")
        time.sleep(1)  # just so we can actually see a message
        await msg.edit("Done! Uninstalled `{}`!".format(modNames))
        args = [EXECUTABLE, "-m", "userbot"]
        os.execle(sys.executable, *args, os.environ)
        await msg.client.disconnect()
        return
    else:
        await msg.edit("Invalid argument! Make sure it is **uninstall**!")
        return


CMD_HELP.update(
    {
        "package manager": [
            'Package Manager',
            " - `pkg uninstall` <py file name>: Remove user modules (modules loaded with the .sideload command)\n\n"
            "**All commands can be used with** `.`"]})

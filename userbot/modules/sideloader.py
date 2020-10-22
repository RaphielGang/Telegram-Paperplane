# Copyright 2020 nunopenim @github
# Copyright 2020 prototype74 @github
#
# Licensed under the PEL (Penim Enterprises License), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the PE License

import sys
import os
import time

from logging import getLogger

from userbot.events import register
from userbot import CMD_HELP

log = getLogger(__name__)
USER_MODULES_DIR = "./userbot/modules_user/"

if " " not in sys.executable:
    EXECUTABLE = sys.executable
else:
    EXECUTABLE = '"' + sys.executable + '"'


@register(outgoing=True, pattern=r"^\.sideload(?: |$)(.*)")
async def sideload(event):
    OVR_WRT_CAUT = True
    cmd_args = event.pattern_match.group(1).split(" ", 1)
    if cmd_args[0].lower() == "force":
        OVR_WRT_CAUT = False
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        file = msg.file
        if not file.name.endswith(".py"):
            await event.edit("This is not a valid .py file! Cannot sideload this!")
            return
        dest_path = USER_MODULES_DIR + file.name
        await event.edit("`Downloading...`")
        if os.path.isfile(dest_path) and OVR_WRT_CAUT:
            log.info(f"Module '{file.name[:-3]}' installed already")
            await event.edit("There is already a userspace module named `{}`. If you wish to overwrite this, please run the command with the `force` argument!".format(file.name))
            return
        await event.client.download_media(message=msg, file=dest_path)
        log.info(f"Module '{file.name[:-3]}' has been installed to userpace")
        await event.edit("Successfully installed `{}`! Rebooting...".format(file.name))
        log.info("Rebooting userbot...")
        time.sleep(1)
        args = [EXECUTABLE, "-m", "userbot"]
        await event.edit("Reboot complete!")
        os.execle(sys.executable, *args, os.environ)
        await event.client.disconnect()
        return
    else:
        await event.edit("Please reply to a valid file!")
        return


CMD_HELP.update(
    {
        "sideloader": [
            'Sideloader',
            " - `sideload`: [in response to a compatible py file] load modules to user space.\n\n"
            "**WARRANTY:** Keep in mind that loading incompatible modules may break your userbot and you will need manual removal of the module.\n"
            "__NO SUPPORT WILL BE OFFERED TO UNOFFICIAL MODULES!__\n\n"
            "**All commands can be used with** `.`"]})

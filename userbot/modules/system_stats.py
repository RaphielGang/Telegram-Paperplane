# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

import kantex
import platform
import shutil
import time
import psutil
import datetime
import sys

from datetime import datetime
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version, uname
from shutil import which

from telethon import __version__, version
from userbot import CMD_HELP, VERSION, ALIVE_NAME, ALIVE_LOGO, bot
from userbot.events import register
from userbot.modules import ALL_MODULES

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern=r"^\.spc")
async def psu(event):
    uname = platform.uname()
    softw = "**System Information**\n"
    softw += f"`System   : {uname.system}`\n"
    softw += f"`Release  : {uname.release}`\n"
    softw += f"`Version  : {uname.version}`\n"
    softw += f"`Machine  : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**CPU Info**\n"
    cpuu += "`Physical cores   : " + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "\n**Total CPU Usage**\n"
    cpuu += f"`All Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memory Usage**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)} ({svmem.percent}%)`\n"
    # Disk Usage
    dtotal, dused, dfree = shutil.disk_usage(".")
    disk = "**Disk Usage**\n"
    disk += f"`Total     : {get_size(dtotal)}`\n"
    disk += f"`Free      : {get_size(dused)}`\n"
    disk += f"`Used      : {get_size(dfree)}`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(disk)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@register(outgoing=True, pattern="^\.sysd$")
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Hella install neofetch first kthx`")


@register(outgoing=True, pattern="^\.botver$")
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())

            await event.edit("`Userbot Version: "
                             f"{verout}"
                             "` \n"
                             "`Revision: "
                             f"{revout}"
                             "` \n"
                             f"`Tagged version: {VERSION}`")
        else:
            await event.edit(
                "Shame that you don't have Git, you're running v1.0 anyway!")


@register(outgoing=True, pattern="^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ For .pip command, do a pip search. """
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            pipc = await asyncrunapp(
                "pip3",
                "search",
                pipmodule,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())

            if pipout:
                if len(pipout) > 4096:
                    await pip.edit("`Output too large, sending as file`")
                    file = open("output.txt", "w+")
                    file.write(pipout)
                    file.close()
                    await pip.client.send_file(
                        pip.chat_id,
                        "output.txt",
                        reply_to=pip.id,
                    )
                    remove("output.txt")
                    return
                await pip.edit("**Query: **\n`"
                               f"pip3 search {pipmodule}"
                               "`\n**Result: **\n`"
                               f"{pipout}"
                               "`")
            else:
                await pip.edit("**Query: **\n`"
                               f"pip3 search {pipmodule}"
                               "`\n**Result: **\n`No Result Returned/False`")
        else:
            await pip.edit("`Use .help pip to see an example`")


@register(outgoing=True, pattern=r"^.(alive|on)$")
async def amireallyalive(alive):
    """
    For .alive command,
    check if the bot is running.
    """
    output = (
        "**Paperplane Minimal**\n"
        f"    **Source:** [HERE](https://github.com/HitaloSama/PaperplaneMinimal) \n"
        f"    **Version:** `{VERSION}` \n"
        f"    **Telethon version:** `{version.__version__}` \n"
        f"    **Python version:** `{python_version()}` \n"
        f"    **KanTeX version:** `{kantex.__version__}` \n"
        f"    **Modules loaded:** `{len(ALL_MODULES)}` \n"
        f"    **User:** `{DEFAULTUSER}`"
    )
    if ALIVE_LOGO:
        await bot.send_file(alive.chat_id, ALIVE_LOGO, caption=output)
        await alive.delete()
    else:
        await alive.edit(output)


@register(outgoing=True, pattern="^\.aliveu")
async def amireallyaliveuser(username):
    """ For .aliveu command, change the username in the .alive command. """
    if not username.text[0].isalpha() and username.text[0] not in ("/", "#",
                                                                   "@", "!"):
        message = username.text
        output = '.aliveu [new user without brackets] nor can it be empty'
        if not (message == '.aliveu' or message[7:8] != ' '):
            newuser = message[8:]
            global DEFAULTUSER
            DEFAULTUSER = newuser
            output = 'Successfully changed user to ' + newuser + '!'
        await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern="^\.resetalive$")
async def amireallyalivereset(ureset):
    """ For .resetalive command, reset the username in the .alive command. """
    if not ureset.text[0].isalpha() and ureset.text[0] not in ("/", "#", "@",
                                                               "!"):
        global DEFAULTUSER
        DEFAULTUSER = uname().node
        await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update({"system stats": ['System Stats',
                                  " - `sysd`: Show system information using neofetch.\n"
                                  " - `botver`: Show Paperplane version.\n"
                                  " - `pip` <module(s)>: Search module(s) in PyPI.\n"
                                  " - `alive`: Check if Paperplane is running.\n"
                                  " - `aliveu` <new_user>: Change the user name in .alive command (aesthetics change only)\n"
                                  " - `spc`: shows some information from your server.\n"
                                  " - `resetalive`: Reset the user name in the .alive command to default (aesthetics change only)\n\n"
                                  "**All commands can be used with** `.`"]
                 })

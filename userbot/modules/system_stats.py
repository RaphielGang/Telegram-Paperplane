# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version, uname
from shutil import which

from telethon import version

from userbot import CMD_HELP, VERSION
from userbot.events import register
from userbot.modules import ALL_MODULES

# ================= CONSTANT =================
DEFAULTUSER = uname().node
# ============================================


@register(outgoing=True, pattern="^.sysd$")
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


@register(outgoing=True, pattern="^.botver$")
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


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
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


@register(outgoing=True, pattern=r"^\.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    await alive.edit(
        "**Paperplane Minimal UserBot**\n"
        f"    **Source:** [HERE](https://github.com/HitaloSama/PaperplaneMinimal) \n"
        f"    **Version:** `{VERSION}` \n"
        f"    **Telethon version:** `{version.__version__}` \n"
        f"    **Python version:** `{python_version()}` \n"
        f"    **Modules loaded:** `{len(ALL_MODULES)}` \n"
        f"    **User:** `{DEFAULTUSER}`"
    )


@register(outgoing=True, pattern="^.aliveu")
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


@register(outgoing=True, pattern="^.resetalive$")
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
                                  " - `alive`: Check if Paperplane is running. \n"
                                  " - `aliveu` <new_user>: Change the user name in .alive command (aesthetics change only)\n"
                                  " - `resetalive`: Reset the user name in the .alive command to default (aesthetics change only)\n\n"
                                  "**All commands can be used with** `.`"]
                 })

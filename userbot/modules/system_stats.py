# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which

from telethon import version

from userbot import HELPER
from userbot.events import register


#================= CONSTANT =================
DEFAULTUSER = uname().node
#============================================


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
            fetch = await asyncrunapp(
                neo,
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
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if which("git") is not None:
            invokever = "git describe --all --long"
            ver = await asyncrunapp(
                invokever,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            invokerev = "git rev-list --all --count"
            rev = await asyncrunapp(
                invokerev,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await event.edit(
                "`Userbot Version: "
                f"{verout}"
                "` \n"
                "`Revision: "
                f"{revout}"
                "`"
            )
        else:
            await event.edit(
                "Shame that you don't have git, You're running r2.2a anyway"
            )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ For .pip command, do a pip search. """
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            invokepip = f"pip3 search {pipmodule}"
            pipc = await asyncrunapp(
                invokepip,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await pip.edit(
                "**Query: **\n`"
                f"{invokepip}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit("`Use .help pip to see an example`")


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    if not alive.text[0].isalpha() and alive.text[0] not in ("/", "#", "@", "!"):
        await alive.edit(
            "`"
            "Your bot is running \n\n"
            f"Telethon version: {version.__version__} \n"
            f"Python: {python_version()} \n"
            f"User: {DEFAULTUSER}"
            "`"
            )


@register(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(username):
    """ For .aliveu command, change the username in the .alive command. """
    if not username.text[0].isalpha() and username.text[0] not in ("/", "#", "@", "!"):
        message = username.text
        output = '.aliveu [new user without brackets] nor can it be empty'
        if not (message == '.aliveu' or message[7:8] != ' '):
            newuser = message[8:]
            global DEFAULTUSER
            DEFAULTUSER = newuser
            output = 'Successfully changed user to ' + newuser + '!'
        await username.edit(
            "`"
            f"{output}"
            "`"
        )


@register(outgoing=True, pattern="^.resetalive$")
async def amireallyalivereset(ureset):
    """ For .resetalive command, reset the username in the .alive command. """
    if not ureset.text[0].isalpha() and ureset.text[0] not in ("/", "#", "@", "!"):
        global DEFAULTUSER
        DEFAULTUSER = uname().node
        await ureset.edit(
            "`"
            "Successfully reset user for alive!"
            "`"
        )

HELPER.update({
    "sysd": ".sysd\
    \nUsage: Shows system information using neofetch."
})
HELPER.update({
    "botver": ".botver\
    \nUsage: Shows the userbot version."
})
HELPER.update({
    "pip": ".pip <module(s)>\
    \nUsage: Does a search of pip modules(s)."
})
HELPER.update({
    "alive": ".alive\
    \nUsage: It's used to check if your bot is working or not. \
Use .aliveu <new_user> to change user or .resetalive to reset .alive."
})

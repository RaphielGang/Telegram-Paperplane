# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which

from telethon import version

from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register


#Alive's user global
defaultuser = uname().node
#


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
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
async def bot_ver(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
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

            await e.edit(
                "`Userbot Version: "
                f"{verout}"
                "` \n"
                "`Revision: "
                f"{revout}"
                "`"
            )
        else:
            await e.edit(
                "Shame that you don't have git, You're running r2.2a anyway"
            )


@register(outgoing=True, pattern="^.pip (.+)")
async def pipcheck(pip):
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        await pip.reply("`Searching . . .`")
        invokepip = f"pip3 search {pip.pattern_match_group(1)}"
        pipc = await asyncrunapp(
            invokepip,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await pip.edit(
            "`"
            f"{pipout}"
            "`"
        )


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(
            "`"
            "Your bot is running \n\n"
            f"Telethon version: {version.__version__} \n"
            f"Python: {python_version()} \n"
            f"User: {defaultuser}"
            "`"
            )


@register(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        output = '.aliveu [new user without brackets] nor can it be empty'
        if not (message == '.aliveu' or message[7:8] != ' '):
            newuser = message[8:]
            global defaultuser
            defaultuser = newuser
            output =  'Successfully changed user to ' + newuser + '!'
        await e.edit(
            "`"
            f"{output}"
            "`"
            )


@register(outgoing=True, pattern="^.resetalive$")
async def amireallyalivereset(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        global defaultuser
        defaultuser = uname().node
        await e.edit(
            "`"
            "Successfully reset user for alive!"
            "`"
            )

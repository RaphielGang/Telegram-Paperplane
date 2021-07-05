# Copyright (C) 2019-2021 The Authors
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

from userbot import CMD_HELP, is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude

# ================= CONSTANT =================
DEFAULTUSER = uname().node
# ============================================


@register(outgoing=True, pattern="^.sysd$")
@grp_exclude()
async def sysdetails(sysd):
    """For .sysd command, get system info using neofetch."""
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch", "--stdout", stdout=asyncPIPE, stderr=asyncPIPE
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch on the host first!`")


@register(outgoing=True, pattern="^.botver$")
@grp_exclude()
async def bot_ver(event):
    """For .botver command, get the bot version."""
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git", "describe", "--all", "--long", stdout=asyncPIPE, stderr=asyncPIPE
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await event.edit(
                f"`Paperplane Version: {verout}`\n" f"`Revision: {revout}`"
            )
        else:
            await event.edit("Install git on the host first!")


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
@grp_exclude()
async def pipcheck(pip):
    """For .pip command, do a pip search."""
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            pipc = await asyncrunapp(
                "pip3", "search", pipmodule, stdout=asyncPIPE, stderr=asyncPIPE
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            if pipout:
                if len(pipout) > 4096:
                    await pip.edit("`Output too large, sending as file`")
                    with open("output.txt", "w+") as output_file:
                        output_file.write(pipout)
                    await pip.client.send_file(
                        pip.chat_id, "output.txt", reply_to=pip.id
                    )
                    remove("output.txt")
                    return
                await pip.edit(
                    "**Query: **\n`"
                    f"pip3 search {pipmodule}"
                    "`\n**Result: **\n`"
                    f"{pipout}"
                    "`"
                )
            else:
                await pip.edit(
                    "**Query: **\n`"
                    f"pip3 search {pipmodule}"
                    "`\n**Result: **\n`No Result Returned/False`"
                )
        else:
            await pip.edit("`Use .help pip to see an example`")


@register(outgoing=True, pattern="^.alive$")
@grp_exclude()
async def amireallyalive(alive):
    if not is_mongo_alive() and not is_redis_alive():
        db = "Both Mongo and Redis Database seems to be failing!"
    elif not is_mongo_alive():
        db = "Mongo DB seems to be failing!"
    elif not is_redis_alive():
        db = "Redis Cache seems to be failing!"
    else:
        db = "Databases functioning normally!"
    await alive.edit(
        "`"
        "Paperplane is running!\n\n"
        f"Telethon version: {version.__version__} \n"
        f"Python version: {python_version()} \n"
        f"User: {DEFAULTUSER} \n"
        f"Database status: {db}\n"
        "`"
    )


@register(outgoing=True, pattern="^.aliveu")
@grp_exclude()
async def amireallyaliveuser(username):
    """For .aliveu command, change the username in the .alive command."""
    if not username.text[0].isalpha() and username.text[0] not in ("/", "#", "@", "!"):
        message = username.text
        output = ".aliveu [new user without brackets] nor can it be empty"
        if not (message == ".aliveu" or message[7:8] != " "):
            newuser = message[8:]
            global DEFAULTUSER
            DEFAULTUSER = newuser
            output = "Successfully changed user to " + newuser + "!"
        await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern="^.resetalive$")
@grp_exclude()
async def amireallyalivereset(ureset):
    """For .resetalive command, reset the username in the .alive command."""
    if not ureset.text[0].isalpha() and ureset.text[0] not in ("/", "#", "@", "!"):
        global DEFAULTUSER
        DEFAULTUSER = uname().node
        await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update(
    {
        "system stats": [
            "System Stats",
            " - `.sysd`: Show system information using neofetch.\n"
            " - `.botver`: Show Paperplane version.\n"
            " - `.pip <module(s)>`: Search module(s) in PyPI.\n"
            " - `.alive`: Check if Paperplane is running. \n"
            " - `.aliveu <new_user>`: Change the user name in .alive command (aesthetics change only)\n"
            " - `.resetalive`: Reset the user name in the .alive command to default (aesthetics change only)\n",
        ]
    }
)

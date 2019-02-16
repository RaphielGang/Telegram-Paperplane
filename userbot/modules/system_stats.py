import asyncio
from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from shutil import which

from telethon import events

from userbot import LOGGER, LOGGER_GROUP, bot


@bot.on(events.NewMessage(outgoing=True, pattern="^.sysd$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sysd$"))
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --stdout"
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


@bot.on(events.NewMessage(outgoing=True, pattern="^.botver$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.botver$"))
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


@bot.on(events.NewMessage(outgoing=True, pattern="^.pip (.+)"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.pip (.+)"))
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

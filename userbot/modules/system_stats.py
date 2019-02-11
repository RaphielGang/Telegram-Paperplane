#########

## PULLING THIS FILE IS NO WAY USEFUL, THIS IS EXCLUSIVELY FOR MY USE

########
import subprocess

import asyncio
from telethon import events

from userbot import LOGGER, LOGGER_GROUP, bot


@bot.on(events.NewMessage(outgoing=True, pattern=".webserverstat"))
@bot.on(events.MessageEdited(outgoing=True, pattern=".webserverstat"))
async def web_server_stat(e):
    result = ""
    if LOGGER:
        result = subprocess.run(
            ["su", "-c", "systemctl", "status", "nginx"],
            stdout=subprocess.PIPE
        ).stdout.decode()
        result = result + "\n\n"
        result = (
            result
            + subprocess.run(
                ["su", "-c", "systemctl", "status", "mariadb"],
                stdout=subprocess.PIPE
            ).stdout.decode()
        )
        result = result + "\n\n"
        result = (
            result
            + subprocess.run(
                ["su", "-c", "systemctl", "status", "postgresql"],
                stdout=subprocess.PIPE
            ).stdout.decode()
        )
        result = result + "\n\n"
        result = (
            result
            + subprocess.run(
                ["su", "-c", "systemctl", "status", "php-fpm"],
                stdout=subprocess.PIPE
            ).stdout.decode()
        )
        f = open("output.txt", "w+")
        f.write(result)
        f.close()
        await bot.send_file(
            LOGGER_GROUP,
            "output.txt",
            reply_to=e.id,
            caption="`Here is your current status`",
        )
        subprocess.run(["rm", "output.txt"], stdout=subprocess.PIPE)
        await e.delete()


@bot.on(events.NewMessage(outgoing=True, pattern="^.sysd$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.sysd$"))
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --stdout"
            fetch = await asyncio.create_subprocess_shell(
                neo,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Hella install neofetch first kthx`")

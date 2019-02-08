#########

## PULLING THIS FILE IS NO WAY USEFUL, THIS IS EXCLUSIVELY FOR MY USE

########
import subprocess

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
        r = (
            "`"
            + subprocess.run(
                [
                    "neofetch",
                    "--off",
                    "--color_blocks off",
                    "--bold off",
                    "--cpu_temp",
                    "C",
                    "--cpu_speed",
                    "on",
                    "--cpu_cores",
                    "physical",
                    "--stdout",
                ],
                stdout=subprocess.PIPE,
            ).stdout.decode()
            + "`"
        )
        await bot.send_message(LOGGER_GROUP, r)
        subprocess.run(["rm", "output.txt"], stdout=subprocess.PIPE)
        await e.delete()

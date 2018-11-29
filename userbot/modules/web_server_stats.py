#########

##PULLING THIS FILE IS NO WAY USEFUL, THIS IS EXCLUSIVELY FOR MY USE

########
import subprocess
from telethon import events
from userbot import bot,LOGGER,LOGGER_GROUP
@bot.on(events.NewMessage(outgoing=True,pattern=".webserverstat"))
@bot.on(events.MessageEdited(outgoing=True,pattern=".webserverstat"))
async def web_server_stat:
    result = ""
    if LOGGER:
        result=subprocess.run("sudo systemctl status nginx", stdout=subprocess.PIPE).stdout.decode()
        result=result+"\n\n"
        result=result+subprocess.run("sudo systemctl status mariadb", stdout=subprocess.PIPE).stdout.decode()
        result=result+"\n\n"
        result=result+subprocess.run("sudo systemctl status postgresql", stdout=subprocess.PIPE).stdout.decode()
        result=result+"\n\n"
        result=result+subprocess.run("sudo systemctl status php-fpm", stdout=subprocess.PIPE).stdout.decode()
        f=open('output.txt', 'w+')
        f.write(result)
        f.close()
        await bot.send_file(LOGGER_GROUP, 'sender.txt', reply_to=e.id, caption="`Here is your current status`")
        subprocess.run(['rm', 'output.txt'], stdout=subprocess.PIPE)
        await e.delete()

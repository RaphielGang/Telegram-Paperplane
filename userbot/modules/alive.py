import asyncio
from userbot.modules.dbhelper import get_a_pic
from platform import python_version

import random
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude

import time
from telethon import version
from userbot import CMD_HELP

#============= Some random function 
async def delete_in(text, seconds): 
    await asyncio.sleep(seconds)    
    return await text.delete()      
#===================================
    

@register(outgoing=True, pattern="alive$")
@grp_exclude()
async def livestatus(alive):
  if not is_mongo_alive() and not is_redis_alive():
    fdb = "Both Mongo db and Redis are malfunctioning!!"
    await alive.edit("**Something's wrong with me...**")
    time.sleep(5)
  if not is_mongo_alive():
    fdb = "Mongo db isn't working right!!"
    await alive.edit("**Something's wrong with me...**")
    time.sleep(5)
  if not is_redis_alive():
    fdb = "Redis seems to be failing!!"
    await alive.edit("Something's wrong with me...")
    time.sleep(5)
  else:
    db = "Databases are functioning smoothly."
    await alive.edit("**I am running all fine~**")
    time.sleep(2)
    x = await alive.edit("***wink***")
    await delete_in(x, 0.5)
  
  ALIVE_IMAGE = await get_a_pic("ALIVE_IMAGE")

  caption = (
            "<u><b>Status🎗</u></b>\n\n"
            f"    <b>|•| Database:</b> <i>{db}</i>\n"
             "         <b>——————————————————————</b>\n"
            f"    <b>|•| Telethon version:</b> <i>{version.__version__}</i>\n"
             "         <b>——————————————————————</b>\n"
            f"    <b>|•| Python version:</b> <i>{python_version()}</i>\n"
             "         <b>——————————————————————</b>\n\n"
             "<b>===========================================</b>\n"
             "<b>Mapleplane is ready to take off🍁</b>"
             "<b>===========================================</b>\n"
  )
  if not db:
      caption = (
            "<u><b>Status🎗</u></b>\n\n"
            f"    <b>|•| Database:</b> <i>{fdb}</i>\n"
             "         <b>——————————————————————</b>\n"
            f"    <b>|•| Telethon version:</b> <i>{version.__version__}</i>\n"
             "         <b>——————————————————————</b>\n"
            f"    <b>|•| Python version:</b> <i>{python_version()}</i>\n"
             "         <b>——————————————————————</b>\n\n"
             "<b>===========================================</b>\n"
             "<b>🔴Mapleplane requires maintainance🔴</b>"
             "<b>===========================================</b>\n"
      )
  
  if ALIVE_IMAGE:
    ALIVE_IMAGE = random.choice(ALIVE_IMAGE)
    await alive.reply(caption, file=ALIVE_IMAGE, parse_mode="html")
  else:
    await alive.reply(caption, parse_mode="html")

    
CMD_HELP.update(
    {
        "alive": [
            "Alive",
            " - `.alive`: Check if your bot is running.\n"
            " - `.setapic <links>`: Set picture for your alive message.\n"
            " - `.getapic`: List all the pictures you have set.\n"
            " - `.delapic`: Delete all the pictures you have set.\n"
        ]
    }
)
 

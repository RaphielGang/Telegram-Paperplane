import asyncio
from userbot.modules.dbhelper import set_a_pic, get_a_pic
from platform import python_version

import random
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude

from telethon import version


@register(outgoing=True, pattern="setapic$")
@grp_exclude()
async def setapic(apic):
  cmd_msg = apic.text
  pic = str(cmd_msg[9: ]).split(" ")
  await set_a_pic(pic, "ALIVE_PIC")
  x = await apic.edit("**ALIVE_PIC has been set!!**")
  asyncio.sleep(5)
  await x.delete()
  return

@register(outgoing=True, pattern="alive$")
@grp_exclude()
async def livestatus(alive):
  if not is_mongo_alive():
    db = "Mongo db isn't working right!!"
  if not is_redis_alive():
    db = "Redis seems to be failing!!"
  if not is_mongo_alive() and not is_redis_alive():
    db = "Both Mongo db and Redis are malfunctioning!!"
  else:
    db = "__Databases are functioning smoothly.__"
    await alive.edit("**I am running all fine~**")
    asyncio.sleep(3)
    x = await alive.edit("*wink*")
    asyncio.sleep(0.5)
    await x.delete() 
    
  ALIVE_PIC = await get_a_pic("ALIVE_PIC") or None
  ALIVE_PIC = random.choice("ALIVE_PIC") or Nne
  
  caption = (
            "Status🎗\n"
            f"    **|•| Database:** {db}\n"
             "         **——————————————————————**\n"
            f"    **|•| Telethon version:** __{version.__version__}__\n"
             "         **——————————————————————**\n"
            f"    **|•| Python version:** __{python_version()}__\n"
             "         **——————————————————————**\n\n"
             "**===========================================**"
             "**Mapleplane is ready to take off🍁**" +
             "**===========================================**"
  )
  
  if ALIVE_PIC:
    await alive.reply(caption, file=ALIVE_PIC)
  else:
    await alive.reply(caption)

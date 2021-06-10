import asyncio
from userbot.modules.dbhelper import set_a_pic, get_a_pic
from platform import python_version

import random
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude

import time
from telethon import version
from userbot import CMD_HELP, VARIABLE

#============= Some random function
async def delete_in(text, seconds):
    await asyncio.sleep(seconds)
    return await text.delete()
#=============

@register(outgoing=True, pattern="setapic")
@grp_exclude()
async def setmyalivepic(apic):
  cmd_msg = apic.text
  pic = str(cmd_msg[9: ]).split(" ")
    
  if pic == "False":
    x = await apic.edit("All pics deleted.")
    return await delete_in(x, 5)

  ALIVE_PIC = "ALIVE_PIC"
  await set_a_pic(pic, ALIVE_PIC):
  x = await apic.edit("ALIVE_PIC has been set!!")
  await delete_in(x, 5)
  return

@register(outgoing=True, pattern="getapic$")
@grp_exclude()
async def myalivepics(apic):
    prv_links = {}
    pics = await get_a_pic("ALIVE_PIC")
    if pics is False:
      x = await apic.edit("You haven't set any pics.")
      return await delete_in(x, 5)
    num_pics = len(pics)
    n = 1
    for i in range(num_pics):
      links = (
        f"PIC {n} - [Link]({pics[i]})\n"
      )
      n += 1
      if "ALIVE_PIC" in VARIABLES:
        VARIABLE["ALIVE_PIC"] += links
      else:
        VARIABLE["ALIVE_PIC"] = links
    mypics = VARIABLE["ALIVE_PIC"]
    message = (
        "<b><u>My Alive Pics</u></b>"
        f"{mypics}"
    )
    await apic.edit(message, parse_mode="html")
    del VARIABLE["ALIVE_PIC"]
    

@register(outgoing=True, pattern="alive$")
@grp_exclude()
async def livestatus(alive):
  if not is_mongo_alive() and not is_redis_alive():
    db = "Both Mongo db and Redis are malfunctioning!!"
    await alive.edit("**Something's wrong with me...**")
    time.sleep(5)
  if not is_mongo_alive():
    db = "Mongo db isn't working right!!"
    await alive.edit("**Something's wrong with me...**")
    time.sleep(5)
  if not is_redis_alive():
    db = "Redis seems to be failing!!"
    await alive.edit("Something's wrong with me...")
    time.sleep(5)
  else:
    db = "Databases are functioning smoothly."
    await alive.edit("**I am running all fine~**")
    time.sleep(2)
    x = await alive.edit("***wink***")
    await delete_in(x, 1)
  
  ALIVE_PIC = "ALIVE_PIC" 
  ALIVE_PIC = await get_a_pic(ALIVE_PIC)
  if ALIVE_PIC == "False":
    ALIVE_PIC = False

  caption = (
            "<u><b>Status🎗</u></b>\n\n"
            f"    <b>|•| Database:</b> <i>{db}</i>\n"
             "         <b>——————————————————————</b>\n"
            f"    <b>|•| Telethon version:</b> <i>{version.__version__}</i>\n"
             "         <b>——————————————————————</b>\n"
            f"    <b>|•| Python version: <i>{python_version()}</i>\n"
             "         <b>——————————————————————</b>\n\n"
             "<b>===========================================</b>\n"
             "<b>Mapleplane is ready to take off🍁</b>"
             "<b>===========================================</b>\n"
  )
  
  if ALIVE_PIC:
    ALIVE_PIC = random.choice(ALIVE_PIC)
    await alive.reply(caption, file=ALIVE_PIC, parse_mode="html")
  else:
    await alive.reply(caption, parse_mode="html")

import time
from userbot import VARIABLES
from userbot.modules.dbhelper import set_a_pic, get_a_pic, del_a_pic

import asyncio
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude

#============= Some random function
async def delete_in(text, seconds):
    await asyncio.sleep(seconds)
    return await text.delete()
#=============

@register(outgoing=True, pattern="setapic")
@grp_exclude()
async def setmyalivepic(apic):
    ALIVE_IMAGE = "ALIVE_IMAGE"
    CMD_MSG = apic.text
    PIC = str(CMD_MSG[9: ]).split(" ")
    await set_a_pic(pic, ALIVE_PIC)
    x = await apic.edit("ALIVE_PIC has been set!!")
    return await delete_in(x, 5)
  
@register(outgoing=True, pattern="getapic$")
@grp_exclude()
async def myalivepics(apic):
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
      if "ALIVE_PIC" in VARIABLE:
        VARIABLE["ALIVE_PIC"] += links
      else:
        VARIABLE["ALIVE_PIC"] = links
        
    mypics = VARIABLE["ALIVE_PIC"]
    message = (
        "**My Alive Pics**\n\n"
        f"{mypics}"
    )
    await apic.edit(message)
    del VARIABLE["ALIVE_PIC"]

@register(outgoing=True, pattern="delapic$")
@grp_exclude()
async def deletemyalivepics(APIC):
    ALIVE_PIC = "ALIVE_PIC"
    
    if del_a_pic(ALIVE_PIC) is False:
        x = await apic.edit("I am sorry but you haven't set any pictures yet.")
        return delete_in(x, 5)
    await del_a_pic(ALIVE_PIC)

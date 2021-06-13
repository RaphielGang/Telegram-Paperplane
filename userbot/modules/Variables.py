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
#=============XXXXXX===============

@register(outgoing=True, pattern="setapic")
@grp_exclude()
async def setmyalivepic(apic):
    ALIVE_IMAGE = "ALIVE_IMAGE"
    CMD_MSG = apic.text
    PIC = str(CMD_MSG[9: ]).split(" ")
    await set_a_pic(PIC, ALIVE_IMAGE)
    x = await apic.edit("Alive pic has been set!!")
    return await delete_in(x, 5)
  
@register(outgoing=True, pattern="getapic$")
@grp_exclude()
async def myalivepics(apic):
    pics = await get_a_pic("ALIVE_IMAGE")
    
    if pics is False:
      x = await apic.edit("You haven't set any pictures.")
      return await delete_in(x, 5)
    
    num_pics = len(pics)
    n = 1
    for i in range(num_pics):
      links = (
        f"PIC {n} - [Link]({pics[i]})\n"
      )
      n += 1
      if "ALIVE_IMAGE" in VARIABLES:
        VARIABLES["ALIVE_IMAGE"] += links
      else:
        VARIABLES["ALIVE_IMAGE"] = links
        
    mypics = VARIABLES["ALIVE_IMAGE"]
    message = (
        "**My Alive Pics**\n\n"
        f"{mypics}"
    )
    await apic.edit(message)
    del VARIABLES["ALIVE_IMAGE"]

@register(outgoing=True, pattern="delapic$")
@grp_exclude()
async def deletemyalivepics(apic):
    ALIVE_IMAGE = "ALIVE_IMAGE"
    
    if await del_a_pic(ALIVE_IMAGE) is False:
        x = await apic.edit("I am sorry but you haven't set any pictures yet.")
        return await delete_in(x, 5)
    await del_a_pic(ALIVE_IMAGE)
    x = await apic.edit("All pictures have been deleted.")
    return await delete_in(x, 5)

@register(outgoing=True, pattern="setpmpic")
@grp_exclude()
async def setmyalivepic(pmpic):
    PM_PERMIT_IMAGE = "PM_PERMIT_IMAGE"
    CMD_MSG = pmpic.text
    PIC = str(CMD_MSG[10: ]).split(" ")
    await set_a_pic(PIC, PM_PERMIT_IMAGE)
    x = await pmpic.edit("PMPermit pic has been set!!")
    return await delete_in(x, 5)
  
@register(outgoing=True, pattern="getpmpic$")
@grp_exclude()
async def myalivepics(pmpic):
    pics = await get_a_pic("PM_PERMIT_IMAGE")
    
    if pics is False:
      x = await pmpic.edit("You haven't set any pictures.")
      return await delete_in(x, 5)
    
    num_pics = len(pics)
    n = 1
    for i in range(num_pics):
      links = (
        f"PIC {n} - [Link]({pics[i]})\n"
      )
      n += 1
      if "PM_PERMIT_IMAGE" in VARIABLES:
        VARIABLES["PM_PERMIT_IMAGE"] += links
      else:
        VARIABLES["PM_PERMIT_IMAGE"] = links
        
    mypics = VARIABLES["PM_PERMIT_IMAGE"]
    message = (
        "**My PMPermit Pics**\n\n"
        f"{mypics}"
    )
    await pmpic.edit(message)
    del VARIABLES["PM_PERMIT_IMAGE"]

@register(outgoing=True, pattern="delpmpic$")
@grp_exclude()
async def deletemyalivepics(pmpic):
    PM_PERMIT_IMAGE = "PM_PERMIT_IMAGE"
    
    if await del_a_pic(PM_PERMIT_IMAGE) is False:
        x = await pmpic.edit("I am sorry but you haven't set any pictures yet.")
        return await delete_in(x, 5)
    await del_a_pic(PM_PERMIT_IMAGE)
    x = await pmpic.edit("All pictures have been deleted.")
    return await delete_in(x, 5)

##
""" Please don't look here, it's so messed up honestly. """
##

import time
from userbot import BOTLOG
from userbot.modules.dbhelper import set_a_pic, get_a_pic, del_a_pic

import asyncio
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude

#============= Some random function
async def delete_in(text, seconds):
    await asyncio.sleep(seconds)
    return await text.delete()
#=============XXXXXX===============

## No Comments ##
ADD_ALIVE_IMAGE = "**Your {} Alive Image{} {} been set.**"
DEL_ALIVE_IMAGE = "**I deleted all the Alive Images.**"
NO_ALIVE
ADD_PMPERMIT_PIC = "**Your {} PM-Permit Image{} {} been set.**"
DEL_PMPERMIT_IMAGES = "**I deleted all the PM-Permit Images.**"

## ........... ##

async def whatpicamisetting(event, pic):
    """Please ignore the name of the func and 2nd arg"""
    if pic == "ALIVE_IMAGE":
        return ADD_ALIVE_IMAGE
    if pic == "PMPERMIT_IMAGE":
        return ADD_PMPERMIT_IMAGE
    
async def iwillsetpic(event, pic, num):
    """This is the function which will set the pictures."""
    try:
        LINKS = str(event.text[num: ]).split("|")
    except:
        if event.reply_to_msg_id:
            MSG = (await event.get_reply_message()).text
            if not MSG:
                x = await event.edit("I am sorry, I really can't find any link whatsoever.")
                return await delete_in(x, 5)
            else:
                LINKS = str(MSG).split("|")
        else:
            x = await event.edit("I am sorry, I really can't find any link whatsoever.")
            return await delete_in(x, 5)
    
    await set_a_pic(LINKS, f"{pic}")
    
    MSG = await whatpicamisetting(event, pic)
    NUML = len(LINKS)
    
    if NUML == 1:
        MSG = MSG.format("1", "", "has")
    else:
        MSG = MSG.format(f"{NUML}", "s", "have")
        
    message = await event.edit(MSG)
    return await delete_in(message, 5)

async def whatpicamideleting(event, pic):
    if pic == "ALIVE_IMAGE":
        return DEL_ALIVE_IMAGE
    if pic == "PMPERMIT_IMAGE":
        return DEL_PMPERMIT_IMAGE
    
async def iwilldeletepic(event, pic):
    """It will delete all the pictures you have set"""
    await del_a_pic(f"{pic}")
    MSG = whatpicamideleting(event, pic)
    message = await event.edit(MSG)
    return await delete_in(message, 5)

async def iwillgetpic(event, pic):
    """It will print out all the pictures you have set."""
    PICS = (await get_a_pic(f"{pic}")).split("|")
    NUMP = len(PICS)
    
    if NUMP == 0:
        await event.edit("**You haven't set any pics
    

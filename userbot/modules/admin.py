from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from telethon.errors import UserAdminInvalidError
from telethon.errors import ChatAdminRequiredError
from telethon.errors import ChannelInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChannelAdminRights
import time
@bot.on(events.NewMessage(outgoing=True,pattern=".wizard"))
@bot.on(events.MessageEdited(outgoing=True,pattern='.wizard'))
async def wizzard(e):
    rights = ChannelAdminRights(
    add_admins=True,
    invite_users=True,
    change_info=True,
    ban_users=True,
    delete_messages=True,
    pin_messages=True,
    invite_link=True,
    )
    await e.edit("`Wizard waves his wand!`")
    time.sleep(3)
    await bot(EditAdminRequest(e.chat_id,(await e.get_reply_message()).sender_id,rights))
    await e.edit("A perfect magic has happened!")
@bot.on(events.NewMessage(outgoing=True,pattern=".thanos"))
@bot.on(events.MessageEdited(outgoing=True,pattern='.thanos'))
async def thanos(e):
        rights = ChannelBannedRights(
                             until_date=None,
                             view_messages=True,
                             send_messages=True,
                             send_media=True,
                             send_stickers=True,
                             send_gifs=True,
                             send_games=True,
                             send_inline=True,
                             embed_links=True
                             )
        if (await e.get_reply_message()).sender_id in BRAIN_CHECKER:
            await e.edit("`Ban Error! Couldn\'t ban this user`")
            return
        await e.edit("`Thanos snaps!`")
        time.sleep(5)
        try:
            await bot(EditBannedRequest(e.chat_id,(await e.get_reply_message()).sender_id,rights))
        except UserAdminInvalidError:
          if e.sender_id in BRAIN_CHECKER:
             await e.respond('<triggerban> '+str((await e.get_reply_message()).sender_id))
             return
        except ChatAdminRequiredError:
         if e.sender_id in BRAIN_CHECKER:
             await e.respond('<triggerban> '+str((await e.get_reply_message()).sender_id))
             return
        except ChannelInvalidError:
          if e.sender_id in BRAIN_CHECKER:
             await e.respond('<triggerban> '+str((await e.get_reply_message()).sender_id))
             return
        await e.delete()
        await bot.send_file(e.chat_id,"https://media.giphy.com/media/xUOxfgwY8Tvj1DY5y0/source.gif")
        if LOGGER:
            await bot.send_message(LOGGER_GROUP,str((await e.get_reply_message()).sender_id)+" was banned.")
@bot.on(events.NewMessage(outgoing=True,pattern=".spider"))
@bot.on(events.MessageEdited(outgoing=True,pattern='.spider'))
async def spider(e):
        if (await e.get_reply_message()).sender_id in BRAIN_CHECKER:
            await e.edit("`Mute Error! Couldn\'t mute this user`")
            return
        db=sqlite3.connect("spam_mute.db")
        cursor=db.cursor()
        cursor.execute('''INSERT INTO MUTE VALUES(?,?)''', (int(e.chat_id),int((await e.get_reply_message()).sender_id)))
        db.commit()
        db.close()
        await e.edit("`Spiderman nabs him!`")
        time.sleep(5)
        await e.delete()
        await bot.send_file(e.chat_id,"https://image.ibb.co/mNtVa9/ezgif_2_49b4f89285.gif")
        if LOGGER:
            await bot.send_message(LOGGER_GROUP,str((await e.get_reply_message()).sender_id)+" was muted.")
@bot.on(events.NewMessage(outgoing=True, pattern='.asmon'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.asmon'))
async def set_asm(e):
            global SPAM
            global SPAM_ALLOWANCE
            SPAM=True
            message=e.text
            SPAM_ALLOWANCE=int(message[6:])
            await e.edit("Spam Tracking turned on!")
            await bot.send_message(LOGGER_GROUP,"Spam Tracking is Turned on!")
@bot.on(events.NewMessage(incoming=True,pattern="<triggerban>"))
async def triggered_ban(e):
    message =e.text
    ban_id=int(e.text[13:])
    if e.sender_id in BRAIN_CHECKER:
        rights = ChannelBannedRights(
                             until_date=None,
                             view_messages=True,
                             send_messages=True,
                             send_media=True,
                             send_stickers=True,
                             send_gifs=True,
                             send_games=True,
                             send_inline=True,
                             embed_links=True
                             )
        if ban_id in BRAIN_CHECKER:
            await e.edit("`Sorry Master!`")
            return
        await e.edit("`Command from my Master!`")
        time.sleep(5)
        await bot(EditBannedRequest(e.chat_id,ban_id,rights))
        await e.delete()
        await bot.send_message(e.chat_id,"Job was done, Master! Gimme Cookies!")
@bot.on(events.NewMessage(incoming=True,pattern="<triggermute>"))
async def triggered_mute(e):
    message =e.text
    ban_id=int(e.text[14:])
    if e.sender_id in BRAIN_CHECKER:
        rights = ChannelBannedRights(
                             until_date=None,
                             view_messages=True,
                             send_messages=True,
                             send_media=True,
                             send_stickers=True,
                             send_gifs=True,
                             send_games=True,
                             send_inline=True,
                             embed_links=True
                             )
        if ban_id in BRAIN_CHECKER:
            await e.edit("`Sorry Master!`")
            return
        await e.edit("`Command from my Master!`")
        time.sleep(5)
        await bot(EditBannedRequest(e.chat_id,(await e.get_reply_message()).sender_id,rights))
        await e.delete()
        await bot.send_file(e.chat_id,"Job was done, Master! Gimme Cookies!")
@bot.on(events.NewMessage(outgoing=True, pattern='.speak'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.speak'))
async def unmute(e):
     db=sqlite3.connect("spam_mute.db")
     cursor=db.cursor()
     cursor.execute('''DELETE FROM mute WHERE chat_id=? AND sender=?''', (int(e.chat_id),int((await e.get_reply_message()).sender_id)))
     db.commit()
     await e.edit("```Unmuted Successfully```")
     db.close()
@bot.on(events.NewMessage(incoming=True))
@bot.on(events.MessageEdited(incoming=True))
async def muter(e):
         db=sqlite3.connect("spam_mute.db")
         cursor=db.cursor()
         cursor.execute('''SELECT * FROM MUTE''')
         all_rows = cursor.fetchall()
         for row in all_rows:
            if int(row[0]) == int(e.chat_id):
               if int(row[1]) == int(e.sender_id):
                 await e.delete()
                 return

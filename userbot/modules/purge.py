from async_generator import aclosing
import asyncio
@bot.on(events.NewMessage(outgoing=True, pattern='.fastpurge'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.fastpurge'))
async def fastpurger(e):
        chat = await e.get_input_chat()
        msgs = []
        count =0
        async with aclosing(bot.iter_messages(chat, min_id=e.reply_to_msg_id)) as h:
         async for m in h:
             msgs.append(m)
             count=count+1
             if len(msgs) == 100:
                 await bot.delete_messages(chat, msgs)
                 msgs = []
        if msgs:
         await bot.delete_messages(chat, msgs)
        await bot.send_message(e.chat_id,"`Fast Purge Complete!\n`Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
        if LOGGER:
            await bot.send_message(LOGGER_GROUP,"Purge of "+str(count)+" messages done successfully.")
        time.sleep(2)
        i=1
        async for message in bot.iter_messages(e.chat_id,from_user='me'):
             if i>1:
                 break
             i=i+1
             await message.delete()
@bot.on(events.NewMessage(outgoing=True, pattern='.snipe'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.snipe'))
async def snipe_on(e):
    text= e.text
    text = text[7:]
    global SNIPE_TEXT
    global SNIPER
    global SNIPE_ID
    SNIPER=True
    SNIPE_TEXT=text
    SNIPE_ID=e.chat_id
    await e.edit('`Sniping active on the word '+text+'`')
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,'`Sniping active on the word '+text+' at '+str(e.chat_id)+'`')
@bot.on(events.NewMessage(outgoing=True, pattern='.purgeme'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.purgeme'))
async def purgeme(e):
    message=e.text
    count = int(message[9:])
    i=1
    async for message in bot.iter_messages(e.chat_id,from_user='me'):
        if i>count+1:
            break
        i=i+1
        await message.delete()
    await bot.send_message(e.chat_id,"`Purge Complete!` Purged "+str(count)+" messages. **This auto-generated message shall be self destructed in 2 seconds.**")
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,"Purge of "+str(count)+" messages done successfully.")
    time.sleep(2)
    i=1
    async for message in bot.iter_messages(e.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
@bot.on(events.NewMessage(outgoing=True, pattern='.delmsg'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.delmsg'))
async def delmsg(e):
        i=1
        async for message in bot.iter_messages(e.chat_id,from_user='me'):
            if i>2:
                break
            i=i+1
            await message.delete()
@bot.on(events.NewMessage(outgoing=True, pattern='.nosnipe'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.nosnipe'))
async def nosnipe(e):
                global SNIPE_TEXT
                global SNIPER
                global SNIPER_ID
                SNIPER=False
                SNIPE_TEXT=""
                SNIPER_ID=0
                await e.edit('`Sniping Turned Off!`')
@bot.on(events.NewMessage(outgoing=True, pattern='.editme'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.editme'))
async def editer(e):
   message=e.text
   string = str(message[8:])
   i=1
   async for message in bot.iter_messages(e.chat_id,from_user='me'):
    if i==2:
        await message.edit(string)
        await e.delete()
        break
    i=i+1
   if LOGGER:
         await bot.send_message(LOGGER_GROUP,"Edit query was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='.sd'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.sd'))
async def selfdestruct(e):
    message=e.text
    counter=int(message[4:6])
    text=str(e.text[6:])
    text=text+"`This message shall be self-destructed in "+str(counter)+" seconds`"
    await e.delete()
    await bot.send_message(e.chat_id,text)
    time.sleep(counter)
    i=1
    async for message in bot.iter_messages(e.chat_id,from_user='me'):
        if i>1:
            break
        i=i+1
        await message.delete()
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,"sd query done successfully")

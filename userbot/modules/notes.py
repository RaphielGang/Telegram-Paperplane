from telethon import events

from userbot import LOGGER, LOGGER_GROUP, bot


@bot.on(events.NewMessage(outgoing=True, pattern="^\.saved$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^\.saved$"))
async def notes_active(svd):
    if not svd.text[0].isalpha() and svd.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.notes_sql import get_notes
        except:
            await svd.edit("`Running on Non-SQL mode!`")
            return

        notes = get_notes(svd.chat_id)
        message = '`There are no saved notes in this chat`'
        if notes:
            message = "Messages saved in this chat: \n\n"
            for note in notes:
                message = message + "🔹 " + note.keyword + "\n"
        await svd.edit(message)


@bot.on(events.NewMessage(outgoing=True, pattern="^\.clear (\w*)"))
async def remove_notes(clr):
    if not clr.text[0].isalpha() and clr.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.notes_sql import rm_note
        except:
            await clr.edit("`Running on Non-SQL mode!`")
            return
        notename = clr.pattern_match.group(1)
        rm_note(clr.chat_id, notename)
        await clr.edit("```Note removed successfully```")


@bot.on(events.NewMessage(outgoing=True, pattern="^\.save (\w*)"))
async def add_filter(fltr):
    if not fltr.text[0].isalpha():
        try:
            from userbot.modules.sql_helper.notes_sql import add_note
        except:
            await fltr.edit("`Running on Non-SQL mode!`")
            return
        notename = fltr.pattern_match.group(1)
        string = fltr.text.partition(notename)[2]
        if fltr.reply_to_msg_id:
            rep_msg = await fltr.get_reply_message()
            string = rep_msg.text
        add_note(str(fltr.chat_id), notename, string)
        await fltr.edit(
            "`Note added successfully. Use` #{} `to get it`".format(notename)
            )


@bot.on(events.NewMessage(pattern="#\w*"))
async def incom_note(getnt):
    try:
        if not (await getnt.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_notes
            except:
                return
            notename = getnt.text[1:]
            notes = get_notes(getnt.chat_id)
            for note in notes:
                if notename == note.keyword:
                    await getnt.reply(note.reply)
                    return
    except:
        pass


@bot.on(events.NewMessage(outgoing=True, pattern="^\.rmnotes$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^\.rmnotes$"))
async def purge_notes(prg):
    try:
        from userbot.modules.sql_helper.notes_sql import rm_all_notes
    except:
        await prg.edit("`Running on Non-SQL mode!`")
        return
    if not prg.text[0].isalpha():
        await prg.edit("```Purging all notes.```")
        rm_all_notes(str(prg.chat_id))
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "I cleaned all notes at " + str(prg.chat_id)
            )

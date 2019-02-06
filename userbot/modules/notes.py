import sqlite3

from telethon import TelegramClient, events

from userbot import LOGGER, LOGGER_GROUP, bot


@bot.on(events.NewMessage(outgoing=True, pattern="^\.saved$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^\.saved$"))
async def notes_active(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.notes_sql import get_notes
        except:
            await e.edit("`Running on Non-SQL mode!`")
            return

        notes = get_notes(e.chat_id)
        message = '`There are no saved notes in this chat`'
        if notes:
            message = "Messages saved in this chat: \n\n"
            for note in notes:
                message = message + "🔹 " + note.keyword + "\n"
        await e.edit(message)


@bot.on(events.NewMessage(outgoing=True, pattern="^\.clear (\w*)"))
async def remove_notes(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.notes_sql import rm_note
        except:
            await e.edit("`Running on Non-SQL mode!`")
            return
        notename = e.pattern_match.group(1)
        rm_note(e.chat_id, notename)
        await e.edit("```Note removed successfully```")


@bot.on(events.NewMessage(outgoing=True, pattern="^\.save (\w*)"))
async def add_filter(e):
    if not e.text[0].isalpha():
        try:
            from userbot.modules.sql_helper.notes_sql import add_note
        except:
            await e.edit("`Running on Non-SQL mode!`")
            return
        notename = e.pattern_match.group(1)
        string = e.text.partition(notename)[2]
        if e.reply_to_msg_id:
            rep_msg = await e.get_reply_message()
            string = rep_msg.text
        add_note(str(e.chat_id), notename, string)
        await e.edit("`Note added successfully. Use` #{} `to get it`".format(notename))


@bot.on(events.NewMessage(pattern="#\w*"))
async def incom_note(e):
    try:
        if not (await e.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_notes
            except:
                return
            notename = e.text[1:]
            notes = get_notes(e.chat_id)
            for note in notes:
                if notename == note.keyword:
                    await e.reply(note.reply)
                    return
    except:
        pass


@bot.on(events.NewMessage(outgoing=True, pattern="^\.rmnotes$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^\.rmnotes$"))
async def purge_notes(e):
    try:
        from userbot.modules.sql_helper.notes_sql import rm_all_notes
    except:
        await e.edit("`Running on Non-SQL mode!`")
        return
    if not e.text[0].isalpha():
        await e.edit("```Purging all notes.```")
        rm_all_notes(str(e.chat_id))
        if LOGGER:
            await bot.send_message(
                LOGGER_GROUP, "I cleaned all notes at " + str(e.chat_id)
            )

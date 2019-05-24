# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module containing commands for keeping notes. """

from userbot import BOTLOG, BOTLOG_CHATID, HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.saved$")
async def notes_active(svd):
    """ For .saved command, list all of the notes saved in a chat. """
    if not svd.text[0].isalpha() and svd.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await svd.edit("`Database connections failing!`")
            return
        notes = get_notes(svd.chat_id)
        message = '`There are no saved notes in this chat.`'
        if notes:
            message = "Notes saved in this chat: \n\n"
            for note in notes:
                message = message + "🔹 " + note['name'] + "\n"
        await svd.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(clr):
    """ For .clear command, clear note with the given name."""
    if not clr.text[0].isalpha() and clr.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await clr.edit("`Database connections failing!`")
            return
        notename = clr.pattern_match.group(1)
        old = MONGO.bot.notes.find_one({"chat_id": clr.chat_id, "name": notename})
        if old:
            MONGO.bot.notes.delete_one({'_id': old['_id']})
            await clr.edit("Note removed successfully")
        else:
            await clr.edit("I can't find this note!")


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_filter(fltr):
    """ For .save command, saves notes in a chat. """
    if not fltr.text[0].isalpha() and fltr.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await fltr.edit("`Database connections failing!`")
            return

        notename = fltr.pattern_match.group(1)
        string = fltr.text.partition(notename)[2]
        if fltr.reply_to_msg_id:
            rep_msg = await fltr.get_reply_message()
            string = rep_msg.text
        old = MONGO.bot.notes.find_one(
            {"chat_id": fltr.chat_id, "name": notename}
            )
        if old:
            status = "updated"
        else:
            status = "saved"
        MONGO.bot.notes.insert_one(
            {"chat_id": fltr.chat_id, "name": notename, "text": string}
            )
        await fltr.edit(
            "`Note added successfully. Use` #{} `to get it`".format(notename)
        )


@register(incoming=True, pattern=r"#\w*", disable_edited=True)
async def incom_note(getnt):
    """ Notes logic. """
    try:
        if not (await getnt.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return
            notename = getnt.text[1:]
            note = MONGO.bot.notes.find_one(
                {"chat_id": getnt.chat_id, "name": notename}
                )
            if note:
                    await getnt.reply(note['text'])
    except:
        pass


@register(outgoing=True, pattern="^.rmnotes (.*)")
async def kick_marie_notes(kick):
    """ For .rmfilters command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    if not kick.text[0].isalpha() and kick.text[0] not in ("/", "#", "@", "!"):
        bot_type=kick.pattern_match.group(1)
        if bot_type not in ["marie","rose"]:
            await kick.edit("`That bot is not yet supported!`")
            return
        if not prg.text[0].isalpha():
            await prg.edit("```Purging all notes.```")
            rm_all_notes(str(prg.chat_id))
            if BOTLOG:
                await prg.client.send_message(
                    BOTLOG_CHATID, "I cleaned all notes at " + str(prg.chat_id)
                )

HELPER.update({
    "notes": "\
#<notename>\
\nUsage: Gets the note with name notename\
\n\n.save <notename> <notedata>\
\nUsage: Saves notedata as a note with the name notename\
\n\n.clear <notename>\
\nUsage: Deletes the note with name notename.\
"
})

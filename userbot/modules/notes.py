# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module containing commands for keeping notes. """

from userbot import LOGGER, LOGGER_GROUP, HELPER, MONGO, REDIS, is_mongo_alive, is_redis_alive
from userbot.events import register, noabuse


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
        old = MONGO.notes.find_one({"chat_id": clr.chat_id, "name": notename})
        print(old)
        print(notename, clr.chat_id)
        if old:
            MONGO.notes.delete_one({'_id': old['_id']})
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
        add_note(str(fltr.chat_id), notename, string)

        await fltr.edit(
            "`Note added successfully. Use` #{} `to get it`".format(notename)
        )


@noabuse(incoming=True, pattern=r"#\w*")
async def incom_note(getnt):
    """ Notes logic. """
    try:
        if not (await getnt.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return
            notename = getnt.text[1:]
            notes = get_notes(getnt.chat_id)
            for note in notes:
                if notename == note.keyword:
                    await getnt.reply(note.reply)
                    return
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.rmnotes$")
async def purge_notes(prg):
    if not is_mongo_alive() or not is_redis_alive():
        await prg.edit("`Database connections failing!`")
        return
    if not prg.text[0].isalpha():
        await prg.edit("```Purging all notes.```")
        notes = MONGO.notes.find({"chat_id": prg.chat_id})
        for note in notes:
            await prg.edit("```Removing {}...```".format(note['name']))
            MONGO.notes.delete_one({'_id': note['_id']})
        await prg.edit("```All notes removed!```")
        if LOGGER:
            await prg.client.send_message(
                LOGGER_GROUP, "I cleaned all notes at " + str(prg.chat_id)
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

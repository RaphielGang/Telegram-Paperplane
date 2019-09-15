# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping notes. """

from asyncio import sleep

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import add_note, delete_note, get_note, get_notes


@register(outgoing=True, pattern="^.saved$")
async def notes_active(event):
    """ For .saved command, list all of the notes saved in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    message = "`There are no saved notes in this chat`"
    notes = await get_notes(event.chat_id)
    for note in notes:
        if message == "`There are no saved notes in this chat`":
            message = "Notes saved in this chat:\n"
            message += "🔹 **{}**\n".format(note["name"])
        else:
            message += "🔹 **{}**\n".format(note["name"])

    await event.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(event):
    """ For .clear command, clear note with the given name."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    notename = event.pattern_match.group(1)
    if await delete_note(event.chat_id, notename) is False:
        return await event.edit("`Couldn't find note:` **{}**".format(notename)
                                )
    else:
        return await event.edit(
            "`Successfully deleted note:` **{}**".format(notename))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_filter(event):
    """ For .save command, saves notes in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    notename = event.pattern_match.group(1)
    string = event.text.partition(notename)[2]
    if event.reply_to_msg_id:
        string = " " + (await event.get_reply_message()).text

    msg = "`Note {} successfully. Use` #{} `to get it`"

    if await add_note(event.chat_id, notename, string[1:]) is False:
        return await event.edit(msg.format('updated', notename))
    else:
        return await event.edit(msg.format('added', notename))


@register(outgoing=True, pattern=r"^.note (\w*)")
async def save_note(event):
    """ For .save command, saves notes in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    note = event.text[6:]
    note_db = await get_note(event.chat_id, note)
    if not await get_note(event.chat_id, note):
        return await event.edit("`Note` **{}** `doesn't exist!`".format(note))
    else:
        return await event.edit(" 🔹 **{}** - `{}`".format(
            note, note_db["text"]))


@register(pattern=r"#\w*",
          disable_edited=True,
          ignore_unsafe=True,
          disable_errors=True)
async def note(event):
    """ Notes logic. """
    try:
        if not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return

            notename = event.text[1:]
            note = await get_note(event.chat_id, notename)
            if note:
                await event.reply(note["text"])
    except BaseException:
        pass


@register(outgoing=True, pattern="^.rmnotes (.*)")
async def kick_marie_notes(kick):
    """ For .rmfilters command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    bot_type = kick.pattern_match.group(1)
    if bot_type not in ["marie", "rose"]:
        await kick.edit("`That bot is not yet supported!`")
        return
    await kick.edit("```Will be kicking away all Notes!```")
    await sleep(3)
    resp = await kick.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type == "marie":
            await kick.reply("/clear %s" % (i.strip()))
        if bot_type == "rose":
            i = i.replace('`', '')
            await kick.reply("/clear %s" % (i.strip()))
        await sleep(0.3)
    await kick.respond(
        "```Successfully purged bots notes yaay!```\n Gimme cookies!")
    if BOTLOG:
        await kick.client.send_message(
            BOTLOG_CHATID, "I cleaned all Notes at " + str(kick.chat_id))


CMD_HELP.update({
    "notes":
    "#<notename>"
    "\nUsage: Get the note with name notename"
    "\n\n.save <notename> <notedata>"
    "\nUsage: Save notedata as a note with the name notename"
    "\n\n.clear <notename>"
    "\nUsage: Delete the note with name notename."
})

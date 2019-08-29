# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """
import re
from asyncio import sleep

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive,
                     is_redis_alive)
from userbot.events import register, errors_handler
from userbot.modules.dbhelper import (get_filters, add_filter, delete_filter)


@register(incoming=True, disable_edited=True)
@errors_handler
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                await handler.edit("`Database connections failing!`")
                return
            listes = handler.text.split(" ")
            filters = await get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                for item in listes:
                    pro = re.fullmatch(trigger["keyword"],
                                       item,
                                       flags=re.IGNORECASE)
                    if pro:
                        await handler.reply(trigger["msg"])
                        return
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.filter\\s.*")
@errors_handler
async def add_new_filter(event):
    """ Command for adding a new filter """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return
        message = event.text
        keyword = message.split()
        string = ""
        for i in range(2, len(keyword)):
            string = string + " " + str(keyword[i])

        if event.reply_to_msg_id:
            string = " " + (await event.get_reply_message()).text

        msg = "`Filter` **{}** `{} successfully`"

        if await add_filter(event.chat_id, keyword[1], string[1:]) is True:
            await event.edit(msg.format(keyword[1], 'added'))
        else:
            await event.edit(msg.format(keyword[1], 'updated'))


@register(outgoing=True, pattern="^.stop\\s.*")
@errors_handler
async def remove_filter(event):
    """ Command for removing a filter """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return
        filt = event.text[6:]

        if not await delete_filter(event.chat_id, filt):
            await event.edit("`Filter` **{}** `doesn't exist.`".format(filt))
        else:
            await event.edit(
                "`Filter` **{}** `was deleted successfully`".format(filt))


@register(outgoing=True, pattern="^.rmfilters (.*)")
@errors_handler
async def kick_marie_filter(event):
    """ For .rmfilters command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        bot_type = event.pattern_match.group(1)
        if bot_type not in ["marie", "rose"]:
            await event.edit("`That bot is not yet supported!`")
            return
        await event.edit("```Will be kicking away all Filters!```")
        await sleep(3)
        resp = await event.get_reply_message()
        filters = resp.text.split("-")[1:]
        for i in filters:
            if bot_type == "marie":
                await event.reply("/stop %s" % (i.strip()))
            if bot_type == "rose":
                i = i.replace('`', '')
                await event.reply("/stop %s" % (i.strip()))
            await sleep(0.3)
        await event.respond(
            "```Successfully purged bots filters yaay!```\n Gimme cookies!")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "I cleaned all filters at " + str(event.chat_id))


@register(outgoing=True, pattern="^.filters$")
@errors_handler
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return
        transact = "`There are no filters in this chat.`"
        filters = await get_filters(event.chat_id)
        for filt in filters:
            if transact == "`There are no filters in this chat.`":
                transact = "Active filters in this chat:\n"
                transact += "🔹 **{}** - `{}`\n".format(filt["keyword"],
                                                       filt["msg"])
            else:
                transact += "🔹 **{}** - `{}`\n".format(filt["keyword"],
                                                       filt["msg"])

        await event.edit(transact)


CMD_HELP.update({
    "filters":
    "\
.filters\
\nUsage: List all active filters in this chat.\
\n\n.filter <keyword> <reply message>\
\nUsage: Add a filter to this chat. \
The bot will now reply that message whenever 'keyword' is mentioned. \
If you reply to sticker with keyword, bot will reply with that sticker.\
\nNOTE: all filter keywords are in lowercase.\
\n\n.stop <filter>\
\nUsage: Stops that filter.\
"
})

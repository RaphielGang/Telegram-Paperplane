# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

from asyncio import sleep
from re import fullmatch, IGNORECASE

from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register


@register(incoming=True)
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            try:
                from userbot import MONGO
            except AttributeError:
                await handler.edit("`Running on Non-SQL mode!`")
                return
            listes = handler.text.split(" ")
            filters = MONGO.filters.find_one({'chat_id': handler.chat_id})
            if not filters:
                return
            for trigger in filters['keyword']:
                for item in listes:
                    pro = fullmatch(trigger.keyword, item, flags=IGNORECASE)
                    if pro:
                        await handler.reply(trigger['msg'])
                        return
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.filter\\s.*")
async def add_new_filter(new_handler):
    """ For .filter command, allows adding new filters in a chat """
    if not new_handler.text[0].isalpha() and new_handler.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot import MONGO
        except AttributeError:
            await new_handler.edit("`Running on Non-SQL mode!`")
            return
        message = new_handler.text
        keyword = message.split()
        string = ""
        for i in range(2, len(keyword)):
            string = string + " " + str(keyword[i])
        old = MONGO.filters.find_one({
            'chat_id': new_handler.chat_id,
            'keyword': keyword[1]})
        if old:
            MONGO.user_list.delete_one({'_id': old['_id']})
        MONGO.filters.insert_one({
            'chat_id': new_handler.chat_id,
            'keyword': keyword[1],
            'msg': string
        })
        await new_handler.edit("```Filter added successfully```")


@register(outgoing=True, pattern="^.stop\\s.*")
async def remove_a_filter(r_handler):
    """ For .stop command, allows you to remove a filter from a chat. """
    if not r_handler.text[0].isalpha() and r_handler.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot import MONGO
        except AttributeError:
            await r_handler.edit("`Running on Non-SQL mode!`")
            return
        message = r_handler.text
        kek = message.split(" ")
        old = MONGO.filters.find_one({
            'chat_id': r_handler.chat_id,
            'keyword': kek})
        if old:
            MONGO.user_list.delete_one({'_id': old['_id']})
        await r_handler.edit("```Filter removed successfully```")


@register(outgoing=True, pattern="^.rmfilters$")
async def kick_marie_filter(kick):
    """ For .rmfilters command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    if not kick.text[0].isalpha() and kick.text[0] not in ("/", "#", "@", "!"):
        await kick.edit("```Will be kicking away all Marie filters.```")
        sleep(3)
        resp = await kick.get_reply_message()
        filters = resp.text.split("-")[1:]
        for i in filters:
            await kick.reply("/stop %s" % (i.strip()))
            await sleep(0.3)
        await kick.respond(
            "```Successfully purged bots filters yaay!```\n Gimme cookies!"
        )
        if LOGGER:
            await kick.client.send_message(
                LOGGER_GROUP, "I cleaned all Marie filters at " +
                str(kick.chat_id)
            )


@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot import MONGO
        except AttributeError:
            await event.edit("`Running on Non-SQL mode!`")
            return
        transact = "`There are no filters in this chat.`"
        filters = MONGO.filters.find({'chat_id': event.chat_id})
        for i in filters:
            message = "Active filters in this chat: \n\n"
            transact = message + "🔹 " + i['keyword'] + "\n"
        await event.edit(transact)


HELPER.update({
    "filters": "\
.filters\
\nUsage: List all active filters in this chat.\
\n\n.filter <keyword> <reply message>\
\nUsage: Add a filter to this chat. \
The bot will now reply that message whenever 'keyword' is mentioned. \
If you reply to a sticker with a keyword, the bot will reply with that sticker.\
\nNOTE: all filter keywords are in lowercase.\
\n\n.stop <filter>\
\nUsage: Stops that filter.\
"
})

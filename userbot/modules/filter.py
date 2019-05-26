# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

from asyncio import sleep
from re import fullmatch, IGNORECASE
import pymongo
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, MONGO, REDIS, is_mongo_alive, is_redis_alive
from userbot.events import register


@register(incoming=True, disable_edited=True)
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                await handler.edit("`Database connections failing!`")
                return
            listes = handler.text.split(" ")
            filters = MONGO.bot.filters.find_one({'chat_id': handler.chat_id})
            if not filters:
                return
            for trigger in filters['keyword']:
                for item in listes:
                    pro = re.fullmatch(trigger['keyword'], item, flags=re.IGNORECASE)
                    if pro:
                        await handler.reply(trigger['msg'])
                        return
    except AttributeError:
        pass


@register(outgoing=True, pattern="^.filter\\s.*")
async def add_new_filter(new_handler):
    """ For .filter command, allows adding new filters in a chat """
    if not new_handler.text[0].isalpha() and new_handler.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await new_handler.edit("`Database connections failing!`")
            return
        message = new_handler.text
        keyword = message.split()
        string = ""
        for i in range(2, len(keyword)):
            string = string + " " + str(keyword[i])
        old = MONGO.bot.filters.find_one({
            'chat_id': new_handler.chat_id,
            'keyword': keyword[1]})
        if old:
            MONGO.bot.filters.delete_one({'_id': old['_id']})
        MONGO.bot.filters.insert_one({
            'chat_id': new_handler.chat_id,
            'keyword': keyword[1],
            'msg': string
        })
        await new_handler.edit("```Filter added successfully```")


@register(outgoing=True, pattern="^.stop\\s.*")
async def remove_a_filter(r_handler):
    """ For .stop command, allows you to remove a filter from a chat. """
    if not r_handler.text[0].isalpha() and r_handler.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await r_handler.edit("`Database connections failing!`")
            return
        message = r_handler.text
        kek = message.split(" ")
        old = MONGO.bot.filters.find_one({
            'chat_id': r_handler.chat_id,
            'keyword': kek})
        if old:
            MONGO.bot.filters.delete_one({'_id': old['_id']})
        await r_handler.edit("```Filter removed successfully```")


@register(outgoing=True, pattern="^.rmfilters (.*)")
async def kick_marie_filter(kick):
    """ For .rmfilters command, allows you to kick all \
        Marie(or her clones) filters from a chat. """
    if not kick.text[0].isalpha() and kick.text[0] not in ("/", "#", "@", "!"):
        bot_type=kick.pattern_match.group(1)
        if bot_type not in ["marie","rose"]:
            await kick.edit("`That bot is not yet supported!`")
            return
        await kick.edit("```Will be kicking away all Filters!```")
        sleep(3)
        resp = await kick.get_reply_message()
        filters = resp.text.split("-")[1:]
        for i in filters:
            if bot_type == "marie":   
                await kick.reply("/stop %s" % (i.strip()))
            if bot_type == "rose":
                i = i.replace('`', '')     #### Rose filters are wrapped under this, to make it touch to copy
                await kick.reply("/stop %s" % (i.strip()))
            await sleep(0.3)
        await kick.respond(
            "```Successfully purged bots filters yaay!```\n Gimme cookies!"
        )
        if BOTLOG:
            await kick.client.send_message(
                BOTLOG_CHATID, "I cleaned all filters at " +
                str(kick.chat_id)
            )


@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return
        transact = "`There are no filters in this chat.`"
        filters = MONGO.bot.filters.find({'chat_id': event.chat_id})
        for i in filters:
            message = "Active filters in this chat: \n\n"
            transact = message + "🔹 " + i['keyword'] + "\n"
        await event.edit(transact)

CMD_HELP.update({
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

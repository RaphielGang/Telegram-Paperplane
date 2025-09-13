# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """
import re
from asyncio import sleep

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import MarkDialogUnreadRequest
from telethon.tl.types import Channel

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive, bot
from userbot.events import register, grp_exclude
from userbot.modules.dbhelper import add_filter, delete_filter, get_filters


@register(incoming=True, disable_errors=True, disable_edited=True)
@grp_exclude()
async def filter_incoming_handler(handler):
    """Checks if the incoming message contains handler of a filter"""
    try:
        sender = await handler.get_sender()
        if sender or not isinstance(sender, Channel) and not sender.bot:
            if not is_mongo_alive():
                await handler.edit("`Database connections failing!`")
                return

            filters = await get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = (
                    r"( |^|[^\w])" + re.escape(trigger["keyword"]) + r"( |$|[^\w])"
                )
                if re.search(pattern, handler.text, flags=re.IGNORECASE):
                    chat = await handler.get_chat()
                    full_chat = (await bot(GetFullChannelRequest(chat.id))).full_chat

                    last_read_message = await handler.client.get_messages(
                        entity=chat,
                        min_id=full_chat.read_inbox_max_id,
                        limit=1,
                        reverse=True,
                    )

                    if trigger.get("is_document", False):
                        content_msg = await handler.client.get_messages(
                            entity=BOTLOG_CHATID, ids=trigger["msg"]
                        )
                        await handler.client.send_file(
                            entity=handler.chat_id,
                            file=content_msg.media,
                            caption=trigger["caption"],
                            reply_to=handler.message.id,
                        )
                    else:
                        await handler.reply(str(trigger["msg"]))

                    # Mark chat as unread after sending the response
                    await handler.client(
                        MarkDialogUnreadRequest(peer=handler.chat_id, unread=True)
                    )

                    if BOTLOG and last_read_message[0]:
                        message_link = (
                            f"https://t.me/c/{chat.id}/{last_read_message[0].id}"
                        )
                        log_message = f"Filter triggered in {chat.title}. Last read message: {message_link}"
                        await handler.client.send_message(BOTLOG_CHATID, log_message)

                    return
    except AttributeError:
        pass


DOUBLE_QUOTES = r'(?:“|”|″|")'
RAW_DOUBLE_QUOTES = r'“”″"'


@register(
    outgoing=True,
    pattern=rf"^.filter ([^{RAW_DOUBLE_QUOTES}]*) ?({DOUBLE_QUOTES}(.*){DOUBLE_QUOTES})?",
)
@grp_exclude()
async def add_new_filter(event):
    """Command for adding a new filter"""
    if not is_mongo_alive():
        await event.edit("`Database connections failing!`")
        return

    if not BOTLOG or not BOTLOG_CHATID:
        await event.edit("`A Botlog chat is needed to save filters!`")
        return

    message = event.text
    keyword = event.pattern_match.group(1).strip()
    content = event.pattern_match.group(3)
    reply = await event.get_reply_message()
    caption = ""
    is_document = False

    if not keyword:
        await event.edit("`No trigger found!`")
        return

    if not content and not reply:
        await event.edit("`No content found!`")
        return

    if event.pattern_match.group(3):
        content = event.pattern_match.group(3)
        caption = event.pattern_match.group(3)
    elif reply:
        content = reply.text
        caption = reply.text

    if reply:
        if reply.document or reply.photo:
            is_document = True
            content = (await reply.forward_to(BOTLOG_CHATID)).id
    else:
        if event.document or event.photo:
            is_document = True
            content = (await event.forward_to(BOTLOG_CHATID)).id

    if await add_filter(event.chat_id, keyword, content, caption, is_document):
        await event.edit(f"`Filter `**{keyword}**` added successfully`")
    else:
        await event.edit(f"`Filter `**{keyword}**` updated successfully`")


@register(outgoing=True, pattern=r"^.stop (.*)")
@grp_exclude()
async def remove_filter(event):
    """Command for removing a filter"""
    if not is_mongo_alive():
        await event.edit("`Database connections failing!`")
        return
    filt = event.pattern_match.group(1)

    if not await delete_filter(event.chat_id, filt):
        await event.edit("`Filter `**{}**` doesn't exist.`".format(filt))
    else:
        await event.edit("`Filter `**{}**` was deleted successfully`".format(filt))


@register(outgoing=True, pattern=r"^.rmfilters (.*)")
@grp_exclude()
async def kick_marie_filter(event):
    """ For .rmfilters command, allows you to remove all \
        Marie(or her clones) filters from a chat. """
    bot_type = event.pattern_match.group(1)
    if bot_type not in ["marie", "rose"]:
        await event.edit("`That bot is not yet supported!`")
        return
    await event.edit("```Purging all bot filters...```")
    await sleep(3)
    resp = await event.get_reply_message()
    if not resp:
        await event.edit("`Reply to the Filters message sent by the bot.`")
        return
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type == "marie":
            await event.reply("/stop %s" % (i.strip()))
        if bot_type == "rose":
            i = i.replace("`", "")
            await event.reply("/stop %s" % (i.strip()))
        await sleep(0.3)
    await event.respond("```Purged bot's filters!```\n")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "I cleaned all filters at " + str(event.chat_id)
        )


@register(outgoing=True, pattern=r"^.filters$")
@grp_exclude()
async def filters_active(event):
    """For .filters command, lists all of the active filters in a chat."""
    if not is_mongo_alive():
        await event.edit("`Database connections failing!`")
        return
    transact = "`There are no filters in this chat.`"
    filters = await get_filters(event.chat_id)
    for filt in filters:
        if transact == "`There are no filters in this chat.`":
            transact = "Active filters in this chat:\n"
            transact += " • **{}**\n".format(filt["keyword"])
        else:
            transact += " • **{}**\n".format(filt["keyword"])

    await event.edit(transact)


CMD_HELP.update(
    {
        "filters": [
            "Filters",
            " - `.filters`: List all active filters in this chat.\n"
            ' - `.filter <keyword> "<reply message/media>"`: Add a filter to this chat.'
            "Paperplane will reply with <reply message> or <media> whenever <keyword> is mentioned. "
            "You can also reply to a message to get the filter content from it. "
            "NOTE: Filters are case insensitive. Reply message must be in **double** quotes.\n"
            " - `.stop <filter>`: Removes the filter from this chat.\n",
        ]
    }
)

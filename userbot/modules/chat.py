# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing userid, chatid and log commands"""

from time import sleep

from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.userid$")
@errors_handler
async def useridgetter(target):
    """ For .userid command, returns the ID of the target user. """
    if not target.text[0].isalpha() and target.text[0] not in ("/", "#", "@",
                                                               "!"):
        message = await target.get_reply_message()
        if message:
            if not message.forward:
                user_id = message.sender.id
                if message.sender.username:
                    name = "@" + message.sender.username
                else:
                    name = "**" + message.sender.first_name + "**"

            else:
                user_id = message.forward.sender.id
                if message.forward.sender.username:
                    name = "@" + message.forward.sender.username
                else:
                    name = "*" + message.forward.sender.first_name + "*"
            await target.edit("**Name:** {} \n**User ID:** `{}`".format(
                name, user_id))


@register(outgoing=True, pattern="^.chatid$")
@errors_handler
async def chatidgetter(chat):
    """ For .chatid, returns the ID of the chat you are in at that moment. """
    if not chat.text[0].isalpha() and chat.text[0] not in ("/", "#", "@", "!"):
        await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
@errors_handler
async def log(log_text):
    """ For .log command, forwards a message
     or the command argument to the bot logs group """
    if not log_text.text[0].isalpha() and log_text.text[0] not in ("/", "#",
                                                                   "@", "!"):
        if BOTLOG:
            if log_text.reply_to_msg_id:
                reply_msg = await log_text.get_reply_message()
                await reply_msg.forward_to(BOTLOG_CHATID)
            elif log_text.pattern_match.group(1):
                user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
                textx = user + log_text.pattern_match.group(1)
                await bot.send_message(BOTLOG_CHATID, textx)
            else:
                await log_text.edit("`What am I supposed to log?`")
                return
            await log_text.edit("`Logged Successfully`")
        else:
            await log_text.edit(
                "`This feature requires Logging to be enabled!`")
        sleep(2)
        await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
@errors_handler
async def kickme(leave):
    """ Basically it's .kickme command """
    if not leave.text[0].isalpha() and leave.text[0] not in ("/", "#", "@",
                                                             "!"):
        await leave.edit("`Nope, no, no, I go away`")
        await bot(LeaveChannelRequest(leave.chat_id))


CMD_HELP.update({"chatid": "Fetch the current chat's ID"})
CMD_HELP.update({
    "userid":
    "Fetch the ID of the user in reply or the \
original author of a forwarded message."
})
CMD_HELP.update(
    {"log": "Forward the message you've replied to to your \
botlog group."})
CMD_HELP.update({"kickme": "Leave from a targeted group."})

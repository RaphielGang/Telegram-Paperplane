# Copyright (C) 2019-2022 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for managing events.
 One of the main components of the userbot. """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import bot, BOTLOG, BOTLOG_CHATID, LOGS
from userbot.modules.dbhelper import get_exclude


def register(**args):
    """Register a new event."""
    pattern = args.get("pattern")
    disable_edited = args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z'\"]"
    group_only = args.get("group_only", False)
    disable_errors = args.get("disable_errors", False)
    insecure = args.get("insecure", False)
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "group_only" in args:
        del args["group_only"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if "insecure" in args:
        del args["insecure"]

    if pattern and not ignore_unsafe:
        args["pattern"] = args["pattern"].replace(r"^.", unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if check.edit_date and check.is_channel and not check.is_group:
                # Messages sent in channels can be edited by other users.
                # Ignore edits that take place in channels.
                return
            if group_only and not check.is_group:
                await check.respond("`Are you sure this is a group?`")
                return
            if check.via_bot_id and not insecure and check.out:
                # Ignore outgoing messages via inline bots for security reasons
                return
            if (check.message.text or "").startswith(("`", "*", "_", "~")):
                # Ignore formatted messages (monospace, bold, italic, strikethrough)
                return

            try:
                await func(check)
            #
            # HACK HACK HACK
            # Catch StopPropagation to Raise StopPropagation
            # This is needed for AFK to work properly
            # TODO
            # Rewrite events to not pass all exceptions
            #
            except events.StopPropagation:
                raise events.StopPropagation
            # No need to log KeyboardInterrupt as an error
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                await log_error(error=e, event=check, disable_errors=disable_errors)
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


def grp_exclude(force_exclude=False):
    """Check if the chat is excluded."""

    def decorator(func):
        async def wrapper(check):
            exclude = await get_exclude(check.chat_id)
            if exclude is not None:
                LOGS.info(func)
                if force_exclude:
                    LOGS.info("EXCLUDED! force_exclude is True")
                    return

                if exclude["excl_type"] == 2:  # all
                    LOGS.info("EXCLUDED! type=2")
                    return

                if exclude["excl_type"] == 1 and check.out is False:  # in
                    LOGS.info("EXCLUDED! type=1 and check.out is False")
                    return

                LOGS.info("NOT EXCLUDED!")
            await func(check)

        return wrapper

    return decorator


async def log_error(error, event, disable_errors=False):
    LOGS.exception(error)  # Log the error in console
    # Check if we have to disable error logging message.
    if not disable_errors:
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        text = "**Sorry, I encountered an error!**\n"
        link = "[https://t.me/tgpaperplane](Userbot Support Chat)"
        text += "If you want to report it, "
        text += f"just forward this message to {link}.\n"
        text += "I won't log anything except the fact of error and date.\n"

        ftext = "\nDisclaimer:\nThis file is uploaded ONLY here, "
        ftext += "we logged only fact of error and date, "
        ftext += "we respect your privacy. "
        ftext += "You may not report this error if you have "
        ftext += "any confidential data here. No one will see your data "
        ftext += "if you choose not to do so.\n\n"
        ftext += "--------BEGIN USERBOT TRACEBACK LOG--------"
        ftext += "\nDate: " + date
        if event:
            ftext += "\nGroup ID: " + str(event.chat_id)
            ftext += "\nSender ID: " + str(event.sender_id)
            ftext += "\n\nEvent Trigger:\n"
            ftext += str(event.text)
        ftext += "\n\nTraceback info:\n"
        ftext += str(format_exc())
        ftext += "\n\nError text:\n"
        ftext += str(sys.exc_info()[1])
        ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

        command = 'git log --pretty=format:"%an: %s" -5'

        ftext += "\n\n\nLast 5 commits:\n"

        process = await asyncsubshell(
            command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
        )
        stdout, stderr = await process.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())

        ftext += result

        with open("error.log", "w+") as output_file:
            output_file.write(ftext)

        if BOTLOG:
            await bot.send_file(BOTLOG_CHATID, "error.log", caption=text)
        elif event:
            await bot.send_file(event.chat_id, "error.log", caption=text)

        remove("error.log")

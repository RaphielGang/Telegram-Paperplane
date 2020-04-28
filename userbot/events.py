# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
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

from userbot import bot, BOTLOG, BOTLOG_CHATID


def register(**args):
    """ Register a new event. """
    def decorator(func):
        pattern = args.get('pattern', None)
        disable_edited = args.get('disable_edited', False)
        ignore_unsafe = args.get('ignore_unsafe', False)
        unsafe_pattern = r'^[^/!#@\$A-Za-z]'
        group_only = args.get('group_only', False)
        disable_errors = args.get('disable_errors', False)
        insecure = args.get('insecure', False)

        if pattern is not None and not pattern.startswith('(?i)'):
            args['pattern'] = '(?i)' + pattern

        if "disable_edited" in args:
            del args['disable_edited']

        if "ignore_unsafe" in args:
            del args['ignore_unsafe']

        if "group_only" in args:
            del args['group_only']

        if "disable_errors" in args:
            del args['disable_errors']

        if "insecure" in args:
            del args['insecure']

        if pattern:
            if not ignore_unsafe:
                args['pattern'] = pattern.replace('^.', unsafe_pattern, 1)


        async def wrapper(check):
            if check.edit_date and check.is_channel and not check.is_group:
                # Messages sent in channels can be edited by other users.
                # Ignore edits that take place in channels.
                return
            if group_only and not check.is_group:
                await check.respond("`Are you sure this is a group?`")
                return
            if check.via_bot_id and not insecure:
                return

            try:
                await func(check)
            #
            # HACK HACK HACK
            # Raise StopPropagation to Raise StopPropagation
            # This needed for AFK to working properly
            # TODO
            # Rewrite events to not passing all exceptions
            #
            except events.StopPropagation:
                raise events.StopPropagation
            # This exception has to be passed
            except KeyboardInterrupt:
                pass
            except BaseException:
                # Check if we have to disable it.
                # If not silence the log spam on the console,
                # with a dumb except.
                if not disable_errors:
                    process = await asyncsubshell(
                        "git log --pretty=format:\"%an: %s\" -5",
                        stdout=asyncsub.PIPE,
                        stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()

                    link = "[https://t.me/userbot_support](Userbot Support Chat)"

                    text = "**Sorry, I encountered a error!**\n" \
                            f"If you want, you can report this to {link}.\n" \
                            "I won't log anything except for the exception and date. \n\n" \
                            "Disclaimer:\n" \
                            "This file uploaded ONLY here, we logged only fact of error " \
                            "and date, we respect your privacy. You may not report this " \
                            "if this containing any non-disclosure data, no one will " \
                            "see your data. \n\n"

                    traceback = "--------BEGIN USERBOT TRACEBACK LOG--------\n" \
                                f"Date: {strftime('%Y-%m-%d %H:%M:%S', gmtime())} \n" \
                                f"Group ID: {str(check.chat_id)} \n" \
                                f"Sender ID: {str(check.sender_id)} \n" \
                                f"Event Trigger: \n{str(check.text)} \n\n" \
                                f"Traceback Info: \n {str(format_exc())} \n\n" \
                                f"Error Text: {str(sys.exc_info()[1])} \n\n" \
                                "-------- END USERBOT TRACEBACK LOG-------- \n\n" \
                                "Last 5 commits: \n" \
                                f"{str(stdout.decode().strip())}" \
                                f"{str(stderr.decode().strip())}"

                    file = open("error.log", "w+")
                    file.write(traceback)
                    file.close()

                    if BOTLOG:
                        await check.client.send_file(
                            BOTLOG_CHATID,
                            "error.log",
                            caption=text,
                        )
                    else:
                        await check.client.send_file(
                            check.chat_id,
                            "error.log",
                            caption=text,
                        )

                    remove("error.log")
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))

        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator

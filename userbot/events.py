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
from telethon.tl.types import ChannelParticipantsAdmins

from userbot import bot


def register(**args):
    """ Register a new event. """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    ignore_unsafe = args.get('ignore_unsafe', False)
    unsafe_pattern = r'^[^/!#@\$A-Za-z]'
    group_only = args.get('group_only', False)
    disable_errors = args.get('disable_errors', False)
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

    if pattern:
        if not ignore_unsafe:
            args['pattern'] = pattern.replace('^.', unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if group_only and not check.is_group:
                await check.respond("`Are you sure this is a group?`")
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
            # This is a gay exception and must be passed out. So that it doesnt spam chats
            except KeyboardInterrupt:
                pass
            except BaseException:

                # Check if we have to disable it.
                # If not silence the log spam on the console,
                # with a dumb except.

                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**Sorry, I encountered a error!**\n"
                    link = "[https://t.me/userbot_support](Userbot Support Chat)"
                    text += "If you wanna you can report it"
                    text += f"- just forward this message to {link}.\n"
                    text += "I won't log anything except the fact of error and date\n"

                    ftext = "\nDisclaimer:\nThis file uploaded ONLY here, "
                    ftext += "we logged only fact of error and date, "
                    ftext += "we respect your privacy, "
                    ftext += "you may not report this error if you've "
                    ftext += "any confidential data here, noone will see your data\n\n"
                    ftext += "--------BEGIN USERBOT TRACEBACK LOG--------"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup ID: " + str(check.chat_id)
                    ftext += "\nSender ID: " + str(check.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(check.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                    command = "git log --pretty=format:\"%an: %s\" -5"

                    ftext += "\n\n\nLast 5 commits:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

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

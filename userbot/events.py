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

from userbot import LogicWorker, bot


def register(**args):
    """ Register a new event. """
    def decorator(func):
        pattern = args.get('pattern', None)
        disable_edited = args.get('disable_edited', False)
        ignore_unsafe = args.get('ignore_unsafe', False)
        unsafe_pattern = r'^[^/!#@\$A-Za-z]'
        group_only = args.get('group_only', False)
        disable_errors = args.get('disable_errors', False)
        permit_sudo = args.get('permit_sudo', False)

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

        if "permit_sudo" in args:
            del args['permit_sudo']

        if pattern:
            if not ignore_unsafe:
                args['pattern'] = pattern.replace('^.', unsafe_pattern, 1)


        async def wrapper(check):
            if group_only and not check.is_group:
                await check.respond("`Are you sure this is a group?`")
                return
            # Check if the sudo is an admin already,
            # if yes, we can avoid acting to his command.
            # If his admin was limited, its his problem.
            if permit_sudo and not check.out:
                if check.sender_id in LogicWorker:
                    async for user in check.client.iter_participants(
                            check.chat_id, filter=ChannelParticipantsAdmins):
                        if user.id in LogicWorker:
                            return
                    # Announce that you are handling the request
                    await check.respond("`Processing Sudo Request!`")
                else:
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
                    process = await asyncsubshell(
                        "git log --pretty=format:\"%an: %s\" -5",
                        stdout=asyncsub.PIPE,
                        stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()

                    link = "[https://t.me/userbot_support](Userbot Support Chat)"

                    text = f"**Sorry, I encountered a error!**\n \
                            If you want, you can report this to {link}.\n \
                            I won't log anything except for the exception and date. \n\n \
                            Disclaimer:\n \
                            This file uploaded ONLY here, we logged only fact of error \
                            and date, we respect your privacy. You may not report this \
                            if this containing any non-disclosure data, no one will \
                            see your data. \n\n"

                    traceback = f"--------BEGIN USERBOT TRACEBACK LOG--------\n \
                                Date: {strftime('%Y-%m-%d %H:%M:%S', gmtime())} \n \
                                Group ID: {str(check.chat_id)} \n \
                                Sender ID: {str(check.sender_id)} \n \
                                Event Trigger: \n{str(check.text)} \
                                Traceback Info: \n {str(format_exc())} \
                                Error Text: \n {str(sys.exc_info()[1])} \n\n \
                                -------- END USERBOT TRACEBACK LOG-------- \n\n \
                                Last 5 commits: \n \
                                {str(stdout.decode().strip())} \
                                {str(stderr.decode().strip())}"

                    file = open("error.log", "w+")
                    file.write(traceback)
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

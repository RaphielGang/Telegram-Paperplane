from telethon import events
from userbot import bot


def register(**args):
    pattern = args.get('pattern', None)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    def decorator(func):
        bot.add_event_handler(func, events.NewMessage(**args))
        bot.add_event_handler(func, events.MessageEdited(**args))
        return func

    return decorator

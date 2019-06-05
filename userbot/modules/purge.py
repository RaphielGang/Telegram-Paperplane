# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for purging unneeded messages(usually spam or ot). """

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.purge$")
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    if not purg.text[0].isalpha() and purg.text[0] not in ("/", "#", "@", "!"):
        chat = await purg.get_input_chat()
        msgs = []
        count = 0

        async for msg in purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id):
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []

        if msgs:
            await purg.client.delete_messages(chat, msgs)
        done = await purg.client.send_message(
            purg.chat_id,
            "`Fast purge complete!\n`Purged "
            + str(count)
            + " messages. **This auto-generated message shall be self destructed in 2 seconds.**",
        )

        if BOTLOG:
            await purg.client.send_message(
                BOTLOG_CHATID, "Purge of " +
                str(count) + " messages done successfully."
            )
        await sleep(2)
        await done.delete()


@register(outgoing=True, pattern="^.purgeme")
async def purgeme(delme):
    """ For .purgeme, delete x count of your latest message."""
    if not delme.text[0].isalpha() and delme.text[0] not in ("/", "#", "@", "!"):
        message = delme.text
        count = int(message[9:])
        i = 1

        async for message in delme.client.iter_messages(delme.chat_id, from_user='me'):
            if i > count + 1:
                break
            i = i + 1
            await message.delete()

        smsg = await delme.client.send_message(
            delme.chat_id,
            "`Purge complete!` Purged "
            + str(count)
            + " messages. **This auto-generated message shall be self destructed in 2 seconds.**",
        )
        if BOTLOG:
            await delme.client.send_message(
                BOTLOG_CHATID, "Purge of " +
                str(count) + " messages done successfully."
            )
        await sleep(2)
        i = 1
        await smsg.delete()


@register(outgoing=True, pattern="^.del$")
async def delete_it(delme):
    """ For .del command, delete the replied message. """
    if not delme.text[0].isalpha() and delme.text[0] not in ("/", "#", "@", "!"):
        msg_src = await delme.get_reply_message()
        if delme.reply_to_msg_id:
            try:
                await msg_src.delete()
                await delme.delete()
                if BOTLOG:
                    await delme.send_message(
                        BOTLOG_CHATID,
                        "Deletion of message was successful"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await delme.send_message(
                        BOTLOG_CHATID,
                        "Well, I can't delete a message"
                    )


@register(outgoing=True, pattern="^.editme")
async def editer(edit):
    """ For .editme command, edit your last message. """
    if not edit.text[0].isalpha() and edit.text[0] not in ("/", "#", "@", "!"):
        message = edit.text
        chat = await edit.get_input_chat()
        self_id = await edit.client.get_peer_id('me')
        string = str(message[8:])
        i = 1
        async for message in edit.client.iter_messages(chat, self_id):
            if i == 2:
                await message.edit(string)
                await edit.delete()
                break
            i = i + 1
        if BOTLOG:
            await edit.send_message(BOTLOG_CHATID, "Edit query was executed successfully")


@register(outgoing=True, pattern="^.sd")
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[4:6])
        text = str(destroy.text[6:])
        text = (
            text
            + "\n\n`This message shall be self-destructed in "
            + str(counter)
            + " seconds`"
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        await sleep(counter)
        await smsg.delete()
        if BOTLOG:
            await destroy.client.send_message(BOTLOG_CHATID, "sd query done successfully")

CMD_HELP.update({
    'purge': '.purge\
        \nUsage: Purges all messages starting from the reply.'
})

CMD_HELP.update({
    'purgeme': '.purgeme <x>\
        \nUsage: Deletes x amount of your latest messages.'
})

CMD_HELP.update({
    "del": ".del\
\nUsage: Deletes the message you replied to."
})

CMD_HELP.update({
    'editme': ".editme <newmessage>\
\nUsage: Edits the text you replied to with newtext."
})

CMD_HELP.update({
    'sd': '.sd <x> <message>\
\nUsage: Creates a message that selfdestructs in x seconds.\
\nKeep the seconds under 100 since it puts your bot to sleep.'
})

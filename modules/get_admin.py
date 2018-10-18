# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from telethon.tl.types import ChannelParticipantsAdmins, ChatParticipantCreator
from telethon.errors import ChatAdminRequiredError, InputUserDeactivatedError


@bot.on(events.NewMessage(pattern=".get_admin ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Chat**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Admins in {} channel: \n".format(input_str)
        try:
            chat = await bot.get_entity(input_str)
        except ValueError as e:
            await event.edit(str(e))
            return None
    try:
        async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                mentions += f"\n[{x.first_name}](tg://user?id={x.id}) `{x.id}`"
            else:
                mentions += f"\n InputUserDeactivatedError `{x.id}`"
    except ChatAdminRequiredError as e:
        mentions += " " + str(e) + "\n"
    await bot.send_message(
        to_write_chat,
        mentions,
        reply_to=event.message.reply_to_msg_id
    )
    await event.delete()

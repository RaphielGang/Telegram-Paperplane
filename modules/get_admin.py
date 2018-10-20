# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from telethon.tl.types import ChannelParticipantsAdmins, ChatParticipantCreator
from telethon.errors import ChatAdminRequiredError, InputUserDeactivatedError
@bot.on(events.NewMessage(pattern=".get_admin ?(.*)", outgoing=True))
async def get_admin(e):
    if e.fwd_from:
        return
    mentions = "**Admins in this Chat**: \n"
    choice = e.pattern_match.group(1)
    to_write_chat = LOGGER_GROUP
    chat = None
    mentions = "Admins in channel {}: \n".format(str(e.chat_id))
    try:
            chat = await bot.get_entity(input_str)
    except ValueError as ea:
            await e.edit(str(ea))
            return None
    try:
        async for x in bot.iter_participants(e.chat_id, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                mentions += f"\n[{x.first_name}](tg://user?id={x.id}) `{x.id}`"
            else:
                mentions += f"\n InputUserDeactivatedError `{x.id}`"
    except ChatAdminRequiredError as ea:
        mentions += " " + str(ea) + "\n"
    if choice==1:
        await bot.send_message(
        e.chat_id,
        mentions,
        reply_to=e.message.reply_to_msg_id
        )
    else:
      if LOGGER:
        await e.edit("`Sent admin details to Logs!`")
        await bot.send_message(
        to_write_chat,
        mentions
        )
      else:
        await e.edit("`This feature needs Logging to be enabled!`")

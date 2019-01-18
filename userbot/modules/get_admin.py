from telethon import TelegramClient, events
from userbot import bot
from userbot import LOGGER, LOGGER_GROUP
from telethon.tl.types import ChannelParticipantsAdmins, ChatParticipantCreator
from telethon.errors import ChatAdminRequiredError, InputUserDeactivatedError


@bot.on(events.NewMessage(pattern="^.chatadmin (.*)", outgoing=True))
async def get_admin(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        mentions = "**Admins in this Chat**: \n"
        choice = int(e.pattern_match.group(1))
        to_write_chat = LOGGER_GROUP
        chat = None
        mentions = "Admins in channel {}: \n".format(str(e.chat_id))
        try:
            async for x in bot.iter_participants(
                e.chat_id, filter=ChannelParticipantsAdmins
            ):
                if not x.deleted:
                    mentions += f"\n[{x.first_name}](tg://user?id={x.id}) `{x.id}`"
                else:
                    mentions += f"\n InputUserDeactivatedError `{x.id}`"
        except ChatAdminRequiredError as ea:
            mentions += " " + str(ea) + "\n"
        if choice:
            await e.edit(mentions)
        elif LOGGER:
            await e.edit("`Sent admin details to Logs!`")
            await bot.send_message(LOGGER_GROUP, mentions)
        else:
            await e.edit("`This feature needs Logging to be enabled!`")

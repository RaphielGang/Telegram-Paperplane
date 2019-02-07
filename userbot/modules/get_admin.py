from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantsAdmins, ChatParticipantCreator, Chat

from userbot import bot

@bot.on(events.NewMessage(outgoing=True, pattern="^.adminlist"))
async def get_admin(show):
    if not show.text[0].isalpha() and show.text[0] not in ("/", "#", "@", "!"):
        mentions = "Admins in {}: \n".format(show.chat.title or "this chat")
        try:
            async for user in bot.iter_participants(
                    show.chat_id, filter=ChannelParticipantsAdmins
            ):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        await show.edit(mentions)

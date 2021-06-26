import randomstuff

from userbot.events import register, grp_exclude
from userbot import RANDOMSTUFF_API_KEY, MONGO


@register(outgoing=True, pattern="addai$")
@grp_exclude()
async def usersetter(ai):
    """Will assign the ai to a replied user"""
    replied_msg = await ai.get_reply_message()
    user_id = replied_msg.sender.id

    MONGO.ai.insert_one({"user": user_id, "chat": ai.chat_id})

    await ai.edit("Hi")


@register(incoming=True, disable_errors=True)
@grp_exclude()
async def aiworker(ai):
    """Will give ai responses to users"""
    message = ai.message.text
    message_sender = message.sender.id

    search = MONGO.ai.find_one({"user": message_sender, "chat": ai.chat_id})

    if search:
        client = randomstuff.Client(api_key=RANDOMSTUFF_API_KEY)
        response = client.get_ai_response(message)

        await ai.reply(response)


import randomstuff
import time

from userbot.events import register, grp_exclude
from userbot import RANDOMSTUFF_API_KEY, MONGO


@register(outgoing=True, pattern="addai$")
@grp_exclude()
async def usersetter(ai):
    """Will assign the ai to a replied user"""
    replied_msg = await ai.get_reply_message()
    user_id = replied_msg.sender.id
    
    search = MONGO.chatbot.find_one({"user": user_id, "chat": ai.chat_id})

    if search:
        x = await ai.edit("I am already responding to this user.")
        time.sleep(5)
        return await x.delete()
    else:
        MONGO.chatbot.insert_one({"user": user_id, "chat": ai.chat_id})

    await ai.edit("Hello!")

@register(outgoing=True, pattern="rmai$")
@grp_exclude()
async def usersetter(ai):
    """Will assign the ai to a replied user"""
    replied_msg = await ai.get_reply_message()
    user_id = replied_msg.sender.id
    
    search = MONGO.chatbot.find_one({"user": user_id, "chat": ai.chat_id})

    if search:
        x = await ai.edit("Nope, I don't know this user.")
        time.sleep(5)
        return await x.delete()
    else:
        MONGO.chatbot.delete_one({"user": user_id, "chat": ai.chat_id})
        x = await ai.edit("I will not respond to this user.")
        time.sleep(5)
        await x.delete()


@register(incoming=True, disable_errors=True)
@grp_exclude()
async def aiworker(ai):
    """Will give ai responses to users"""
    message = ai.message.text
    message_sender = ai.sender.id

    search = MONGO.chatbot.find_one({"user": message_sender, "chat": ai.chat_id})

    if search:
        client = randomstuff.AsyncClient(api_key=RANDOMSTUFF_API_KEY)
        response = client.get_ai_response(
            message = message,
            master = "Lee",
            bot = "Maple",
            )

        await ai.reply(f"{response}")


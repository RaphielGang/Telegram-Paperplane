"""This is chatbot plugin to make users talk to an AI"""

import randomstuff
import random
import time

from userbot.events import register, grp_exclude
from userbot import RANDOMSTUFF_API_KEY, MONGO




@register(outgoing=True, pattern="addai$")
@grp_exclude()
async def usersetter(ai):
    """Will assign the ai to a replied user"""
    if ai.is_private: user_id = ai.chat_id
    elif ai.reply_to_msg_id:
        replied_msg = await ai.get_reply_message()
        user_id = replied_msg.sender.id
    else:
        await ai.edit("Reply to someone to add ai.")
        time.sleep(5)
        return await ai.delete()

    if not RANDOMSTUFF_API_KEY:
        return await ai.reply("Set `RANDOMSTUFF_API_KEY` variable with a correct value first.")

    search = MONGO.chatbot.find_one({"Chatbot": True, "user": user_id, "chat": ai.chat_id})

    if search:
        await ai.edit("I am already responding to this user.")
        time.sleep(5)
        return await ai.delete()

    MONGO.chatbot.insert_one({"Chatbot": True, "user": user_id, "chat": ai.chat_id})
    await ai.edit("Hello!")

@register(outgoing=True, pattern="rmai$")
@grp_exclude()
async def userremover(ai):
    """Will assign the ai to a replied user"""
    if ai.is_private: user_id = ai.chat_id
    else:
        replied_msg = await ai.get_reply_message()
        user_id = replied_msg.sender.id

    search = MONGO.chatbot.find_one({"Chatbot": True, "user": user_id, "chat": ai.chat_id})

    if not search:
        await ai.edit("Nope, I don't know this user.")
        time.sleep(5)
        return await ai.delete()

    MONGO.chatbot.delete_one({"Chatbot": True, "user": user_id, "chat": ai.chat_id})
    await ai.edit("__AI response stat:__ \n" "**DEACTIVATED**")

    time.sleep(5)
    await ai.delete()

@register(incoming=True, disable_errors=True)
@grp_exclude()
async def aiworker(ai):
    """Will give ai responses to users"""
    message = ai.message.text
    message_sender = ai.sender.id

    search = MONGO.chatbot.find_one({"Chatbot": True, "user": message_sender, "chat": ai.chat_id})

    if not search: return

    if message == "WITH ALL MY MIGHT STOP THE AI":
        MONGO.chatbot.delete_one({"user": message_sender, "chat": ai.chat_id})
        await ai.reply(
            "You got me there! I am rolling back for now, will meet ya later. "
            "***White Flag Hovers 🏳️***"
        )
        time.sleep(8)
        return await ai.delete()

    client = randomstuff.AsyncClient(api_key=RANDOMSTUFF_API_KEY)
    response = await client.get_ai_response(
        message=message,
        master="Lee",
        bot="Maple"
    )
    wait = await chat_action(ai, response)
    await client.close()
    await ai.reply(f"{response.message}")


@register(outgoing=True, pattern="listai")
@grp_exclude()
async def listai(event):
    fake_ls = "List of Users and Chat Id\n"
    search = MONGO.chatbot.find_one("Chatbot": True)
    search_in = MONGO.chatbot.find_one("Chatbot": True, "chat": event.chat_id)
    users = search["user"]
    chats = search["chat"]
    users_in = search_in["user"]
    if search_in:
        ls = "List of users in the current chat are:\n"
        for n in range(users):



# CHAT ACTION #
async def chat_action(worker, response):
    """To make the AI more realistic"""
    text = response.message
    count = len(text)
    wait = count * 0.05

    if wait >= 15:
        wait == 15

    async with worker.client.action(worker.chat_id, 'typing'):
        time.sleep(wait)
    return wait
#   ......    #

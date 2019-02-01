from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import UserFull
import os
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot import bot
from telethon.tl.functions.messages import EditMessageRequest
from telethon.tl.types import User

TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")

@bot.on(events.NewMessage(pattern="\.whois ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    replied_user = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await bot(GetFullUserRequest(previous_message.from_id))
    else:
        input_str = event.pattern_match.group(1)
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if type(probable_user_mention_entity) == MessageEntityMentionName:
                user_id = probable_user_mention_entity.user_id
                replied_user = await bot(GetFullUserRequest(user_id))
            else:
                # the disgusting CRAP way, of doing the thing
                try:
                    user_object = await bot.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await bot(GetFullUserRequest(user_id))
                except Exception as e:
                    await event.edit(str(e))
                    return None
        else:
            try:
                user_object = await bot.get_entity(input_str)
                user_id = user_object.id
                replied_user = await bot(GetFullUserRequest(user_id))
            except Exception as e:
                await event.edit(str(e))
                return None
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name 
    last_name = replied_user.user.last_name
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username 
    user_bio = replied_user.about
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
        photo = await bot.download_profile_photo(
            user_id,
            TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
            download_big=True
        )
    except TypeError as e:
        dc_id = "__ need a Profile Picture for this to work __"
        photo = "https://thumbs.dreamstime.com/b/no-user-profile-picture-24185395.jpg"
    if first_name:
        first_name = first_name.replace("\u2060", "")
    else:
        first_name = "This User has no First Name"
    if last_name:
        last_name = last_name.replace("\u2060", "")
    else:
        last_name = "This User has no Last Name"
    if username:
        username = "@{}".format(username)
    else:
        username= "This User has no Username"
    if user_bio:
        user_bio = user_bio
    else:
        user_bio = "This User has no About" 
    caption = "USER INFO: \n\nFirst Name: {} \nLast Name: {} \nUSERNAME: {} \nID: `{}`  \n\nBio: \n{} \n\nCommon Chats with this user: {} \nPermanent Link To Profile: [Click Here](tg://user?id={})".format(first_name, last_name, username, user_id, user_bio, common_chat, user_id)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await bot.send_file(
        event.chat_id,
        photo,
        caption=caption,
        force_document=False,
        reply_to=message_id_to_reply
    )
    if not photo.startswith("http"):
        os.remove(photo)
    await event.delete()

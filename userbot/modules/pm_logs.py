import asyncio
from telethon import events
from telethon.tl import functions, types
from userbot.events import register
from userbot import BOTLOG, BOTLOG_CHATID, LOGS, PM_LOG_ALLOW

NO_PM_LOG_USERS = []


@register(incoming=True, disable_edited=True)
async def monito_p_m_s(event):
    if PM_LOG_ALLOW:
        pass
    else:
        return

    sender = await event.get_sender()
    if event.is_private and not (await event.get_sender()).bot:
        chat = await event.get_chat()
        self_user = await event.client.get_me()
        DEF_NO_LOG = [777000]
        DEF_NO_LOG.append(int(self_user.id))
        if chat.id in DEF_NO_LOG:
            return

        if chat.id not in NO_PM_LOG_USERS and chat.id:
            if not BOTLOG_CHATID:
                LOG.warn("No log chat specfied. Returning")
                return
            try:
                e = await event.client.get_entity(int(BOTLOG_CHATID))
                fwd_message = await event.client.forward_messages(
                    e, event.message, silent=True)
            except Exception as e:
                LOGS.warn(str(e))

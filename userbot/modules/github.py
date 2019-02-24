import aiohttp
from telethon import events

from userbot import bot

@bot.on(events.NewMessage(outgoing=True, pattern=r"^\.git (.*)"))
async def github(e):

    URL = f"https://api.github.com/users/{e.pattern_match.group(1)}"
    chat = await e.get_chat()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                await e.reply("`" + e.pattern_match.group(1) + " not found`")
                return

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = f"""
        GitHub Info for `{e.pattern_match.group(1)}`

Username: `{name}`
Bio: `{bio}`
URL: {url}
Company: `{company}`
Created at: `{created_at}`
            """
            if not result.get("repos_url", None):
                await bot.send_message(chat.id, message=REPLY, reply_to=e.id, link_preview=False)
                return
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    await e.edit(REPLY)
                    return

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await bot.send_message(chat.id, message=REPLY, reply_to=e.id, link_preview=False)

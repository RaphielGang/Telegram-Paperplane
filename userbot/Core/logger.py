"""Logger hideout"""

from userbot maple_config, maple
from logging import DEBUG, INFO, basicConfig, getLogger

# Bot's Logger.
if maple_config.CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
        datefmt="%H:%M:%S"
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO,
        filename=datefmt="%H:%M:%S"
    )

LOGS = getLogger("MaplePlane")

# This will keep checking BOTLOG and will stop the bot at any error.
async def check_botlog_chatid():
    if not BOTLOG:
        return
    try:
        entity = await maple.get_entity(BOTLOG_CHATID)
    except ValueError:
        LOGS.error(
            "You don't have rights to access BOTLOG("
            + BOTLOG_CHATID +
            ") group. Check if you have typed the correct BOTLOG_CHATID. Halting takeoff!!"
        )
        quit(1)
    if entity.default_banned_rights.send_messages:
        LOGS.error(
            "You don't have rights to send messages to BOTLOG("
            + BOTLOG_CHATID +
            ") group. Check if you have typed the correct BOTLOG_CHATID. Halting takeoff!!"
        )
        quit(1)

with maple:
    maple.loop.run_until_complete(check_botlog_chatid())

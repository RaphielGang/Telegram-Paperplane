import re
import sre_constants

from telethon import events

from userbot import LOGGER, LOGGER_GROUP, bot

DELIMITERS = ("/", ":", "|", "_")


def separate_sed(sed_string):
    if (
            len(sed_string) >= 3
            and sed_string[3] in DELIMITERS
            and sed_string.count(sed_string[3]) >= 2
    ):
        delim = sed_string[3]
        start = counter = 4
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (
                    sed_string[counter] == "\\"
                    and counter + 1 < len(sed_string)
                    and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1 :]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()


@bot.on(events.NewMessage(outgoing=True, pattern="^sed"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^sed"))
async def sed(e):
    sed_result = separate_sed(e.text)
    L = await e.get_reply_message()
    if sed_result:
        if L:
            to_fix = L.text
        else:
            await e.edit(
                "`Master, I don't have brains. Well you too don't I guess.`"
                )
            return

        repl, repl_with, flags = sed_result

        if not repl:
            await e.edit(
                "`Master, I don't have brains. Well you too don't I guess.`"
                )
            return

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                await e.edit(
                    "`Boi!, that's a reply. Don't use sed`"
                    )
                return

            if "i" in flags and "g" in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif "i" in flags:
                text = re.sub(repl, repl_with, to_fix, count=1, flags=re.I).strip()
            elif "g" in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_constants.error:
            LOGGER.warning(e.text)
            LOGGER.exception("SRE constant error")
            await e.edit("B O I! [Learn Regex](https://regexone.com)")
            return
        if text:
            await e.edit("Did you mean? \n\n`" + text + "`")

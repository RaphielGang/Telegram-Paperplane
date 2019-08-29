# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting the date
    and time of any country or the userbot server.  """

from datetime import datetime as dt

from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from userbot import CMD_HELP
from userbot.events import register, errors_handler

# ===== CONSTANT =====
COUNTRY = ''
TZ_NUMBER = 1


# ===== CONSTANT =====
async def get_tz(con):
    """ Get time zone of the given country. """
    if "(Uk)" in con:
        con = con.replace("Uk", "UK")
    if "(Us)" in con:
        con = con.replace("Us", "US")
    if " Of " in con:
        con = con.replace(" Of ", " of ")
    if "(Western)" in con:
        con = con.replace("(Western)", "(western)")
    if "Minor Outlying Islands" in con:
        con = con.replace("Minor Outlying Islands", "minor outlying islands")
    if "Nl" in con:
        con = con.replace("Nl", "NL")

    for c_code in c_n:
        if con == c_n[c_code]:
            return c_tz[c_code]
    try:
        if c_n[con]:
            return c_tz[con]
    except KeyError:
        return


@register(outgoing=True, pattern="^.time(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?")
@errors_handler
async def time_func(tdata):
    """ For .time command, return the time of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    if not tdata.text[0].isalpha() and tdata.text[0] not in ("/", "#", "@",
                                                             "!"):
        con = tdata.pattern_match.group(1).title()
        tz_num = tdata.pattern_match.group(2)

        t_form = "%H:%M"
        c_name = ''

        if con:
            try:
                c_name = c_n[con]
            except KeyError:
                c_name = con

            timezones = await get_tz(con)
        elif COUNTRY:
            c_name = COUNTRY
            tz_num = TZ_NUMBER
            timezones = await get_tz(COUNTRY)
        else:
            await tdata.edit(
                f"`It's`  **{dt.now().strftime(t_form)}**  `here.`")
            return

        if not timezones:
            await tdata.edit("`Invaild country.`")
            return

        if len(timezones) == 1:
            time_zone = timezones[0]
        elif len(timezones) > 1:
            if tz_num:
                tz_num = int(tz_num)
                time_zone = timezones[tz_num - 1]
            else:
                return_str = f"{c_name} has multiple timezones:\n"

                for i, item in enumerate(timezones):
                    return_str += f"{i+1}. {item}\n"

                return_str += "Choose one by typing the number "
                return_str += "in the command. Example:\n"
                return_str += f".time {c_name} 2"

                await tdata.edit(return_str)
                return

        dtnow = dt.now(tz(time_zone)).strftime(t_form)

        if COUNTRY:
            await tdata.edit(f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                             f"({time_zone} timezone).`")
            return

        await tdata.edit(
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`")


@register(outgoing=True, pattern="^.date(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?")
@errors_handler
async def date_func(dat):
    """ For .date command, return the date of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    if not dat.text[0].isalpha() and dat.text[0] not in ("/", "#", "@", "!"):
        con = dat.pattern_match.group(1).title()
        tz_num = dat.pattern_match.group(2)

        d_form = "%d/%m/%y - %A"
        c_name = ''

        if con:
            try:
                c_name = c_n[con]
            except KeyError:
                c_name = con

            timezones = await get_tz(con)
        elif COUNTRY:
            c_name = COUNTRY
            tz_num = TZ_NUMBER
            timezones = await get_tz(COUNTRY)
        else:
            await dat.edit(f"`It's`  **{dt.now().strftime(d_form)}**  `here.`")
            return

        if not timezones:
            await dat.edit("`Invaild country.`")
            return

        if len(timezones) == 1:
            time_zone = timezones[0]
        elif len(timezones) > 1:
            if tz_num:
                tz_num = int(tz_num)
                time_zone = timezones[tz_num - 1]
            else:
                return_str = f"{c_name} has multiple timezones:\n"

                for i, item in enumerate(timezones):
                    return_str += f"{i+1}. {item}\n"

                return_str += "Choose one by typing the number "
                return_str += "in the command. Example:\n"
                return_str += f".date {c_name} 2"

                await dat.edit(return_str)
                return

        dtnow = dt.now(tz(time_zone)).strftime(d_form)

        if COUNTRY:
            await dat.edit(f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                           f"({time_zone} timezone).`")
            return

        await dat.edit(
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`")


@register(outgoing=True, pattern="^.settime (.*)(?<![0-9])(?: |$)([0-9]+)?")
@errors_handler
async def set_time_country(loc):
    """ For .settime command, change the default userbot
        country for date and time commands. """
    if not loc.text[0].isalpha() and loc.text[0] not in ("/", "#", "@", "!"):
        global COUNTRY
        global TZ_NUMBER
        temp_country = loc.pattern_match.group(1).title()
        temp_tz_num = loc.pattern_match.group(2)

        try:
            c_name = c_n[temp_country]
        except KeyError:
            c_name = temp_country

        timezones = await get_tz(temp_country)

        if not timezones:
            await loc.edit("`Invaild country.`")
            return

        if len(timezones) == 1:
            TZ_NUMBER = 1
        elif len(timezones) > 1:
            if temp_tz_num:
                TZ_NUMBER = int(temp_tz_num)
            else:
                return_str = f"{c_name} has multiple timezones:\n"

                for i, item in enumerate(timezones):
                    return_str += f"{i+1}. {item}\n"

                return_str += "Choose one by typing the number "
                return_str += "in the command. Example:\n"
                return_str += f".settime {c_name} 2"

                await loc.edit(return_str)
                return

        COUNTRY = c_name
        tz_name = timezones[TZ_NUMBER - 1]

        await loc.edit("`Default country for date and time set to "
                       f"{COUNTRY}({tz_name} timezone).`")


CMD_HELP.update({
    "time":
    ".time <country name/code> <timezone number>"
    "\nUsage: Get the time of a country. If a country has "
    "multiple timezones, Paperplane will list all of them "
    "and let you select one."
})
CMD_HELP.update({
    "date":
    ".date <country name/code> <timezone number>"
    "\nUsage: Get the date of a country. If a country has "
    "multiple timezones, Paperplane will list all of them "
    "and let you select one."
})
CMD_HELP.update({
    "settime":
    ".settime <country name/code> <timezone number>"
    "\nUsage: Set the default country for .time and .date "
    "command. If a country has multiple timezones, Paperpl"
    "ane will list all of them and let you select one."
})

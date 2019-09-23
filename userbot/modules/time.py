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

from userbot import CMD_HELP, is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import get_time, set_time

# ===== CONSTANT =====
INV_CON = "`Invalid country.`"
TZ_NOT_FOUND = "`The selected timezone is not found! Try again!`"
DB_FAILED = "`Database connections failed!`"


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
async def time_func(tdata):
    """ For .time command, return the time of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    con = tdata.pattern_match.group(1).title()
    tz_num = tdata.pattern_match.group(2)

    t_form = "%H:%M"

    saved_props = await get_time() if is_mongo_alive() else None
    saved_country = saved_props['timec'] if saved_props else None
    saved_tz_num = saved_props['timezone'] if saved_props else None

    if con:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con

        timezones = await get_tz(con)
    elif saved_country:
        c_name = saved_country
        tz_num = saved_tz_num
        timezones = await get_tz(saved_country)
    else:
        await tdata.edit(f"`It's`  **{dt.now().strftime(t_form)}**  `here.`")
        return

    if not timezones:
        await tdata.edit(INV_CON)
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            if len(timezones) >= tz_num:
                time_zone = timezones[tz_num - 1]
            else:
                await tdata.edit(TZ_NOT_FOUND)
                return
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

    if not con and saved_country:
        await tdata.edit(f"`It's`  **{dtnow}**  `here, in {saved_country}"
                         f"({time_zone} timezone).`")
        return

    await tdata.edit(
        f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`")


@register(outgoing=True, pattern="^.date(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?")
async def date_func(dat):
    """ For .date command, return the date of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    con = dat.pattern_match.group(1).title()
    tz_num = dat.pattern_match.group(2)

    d_form = "%d/%m/%y - %A"

    saved_props = await get_time() if is_mongo_alive() else None
    saved_country = saved_props['timec'] if saved_props else None
    saved_tz_num = saved_props['timezone'] if saved_props else None

    if con:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con

        timezones = await get_tz(con)
    elif saved_country:
        c_name = saved_country
        tz_num = saved_tz_num
        timezones = await get_tz(saved_country)
    else:
        await dat.edit(f"`It's`  **{dt.now().strftime(d_form)}**  `here.`")
        return

    if not timezones:
        await dat.edit(INV_CON)
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            if len(timezones) >= tz_num:
                time_zone = timezones[tz_num - 1]
            else:
                await dat.edit(TZ_NOT_FOUND)
                return
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

    if not con and saved_country:
        await dat.edit(f"`It's`  **{dtnow}**  `here, in {saved_country}"
                       f"({time_zone} timezone).`")
        return

    await dat.edit(f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`"
                   )


@register(outgoing=True, pattern="^.settime (.*)(?<![0-9])(?: |$)([0-9]+)?")
async def set_time_country(loc):
    """ For .settime command, change the default userbot
        country for date and time commands. """
    if not is_mongo_alive() or not is_redis_alive():
        await loc.edit(DB_FAILED)
        return

    temp_country = loc.pattern_match.group(1).title()
    temp_tz_num = loc.pattern_match.group(2)

    c_name = None
    tz_num = None

    try:
        c_name = c_n[temp_country]
    except KeyError:
        c_name = temp_country

    timezones = await get_tz(temp_country)

    if not timezones:
        await loc.edit(INV_CON)
        return

    if len(timezones) == 1:
        tz_num = 1
    elif len(timezones) > 1:
        if temp_tz_num:
            tz_num = int(temp_tz_num)
        else:
            return_str = f"{c_name} has multiple timezones:\n"

            for i, item in enumerate(timezones):
                return_str += f"{i+1}. {item}\n"

            return_str += "Choose one by typing the number "
            return_str += "in the command. Example:\n"
            return_str += f".settime {c_name} 2"

            await loc.edit(return_str)
            return

    if len(timezones) >= tz_num:
        tz_name = timezones[tz_num - 1]
    else:
        await loc.edit(TZ_NOT_FOUND)
        return

    await set_time(c_name, tz_num)

    await loc.edit("`Default country for date and time set to "
                   f"{c_name}({tz_name} timezone).`")


CMD_HELP.update({
    "time":
    ".time <country name/code> <timezone number>\n"
    "Usage: Get the time of a country. If a country has "
    "multiple timezones, Paperplane will list all of them "
    "and let you select one."
})
CMD_HELP.update({
    "date":
    ".date <country name/code> <timezone number>\n"
    "Usage: Get the date of a country. If a country has "
    "multiple timezones, Paperplane will list all of them "
    "and let you select one."
})
CMD_HELP.update({
    "settime":
    ".settime <country name/code> <timezone number>\n"
    "Usage: Set the default country for .time and .date "
    "command. If a country has multiple timezones, Paperpl"
    "ane will list all of them and let you select one."
})

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for getting the date and time of any country or the userbot server.  """

from datetime import datetime as dt
from pytz import country_names as c_n, country_timezones as c_tz, timezone as tz
from userbot.events import register

COUNTRY = ''

async def get_tz(con):
    """ Get time zone of the given country. """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return

@register(outgoing=True, pattern="^.time ?(.*)")
async def time_func(tdata):
    """ For .time command, return the time of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .ctime),
        3. The server where the userbot runs.
    """
    if not tdata.text[0].isalpha() and tdata.text[0] not in ("/", "#", "@", "!"):
        con = tdata.pattern_match.group(1).title()
        t_form = "%I:%M %p"

        if not con:
            if not COUNTRY:
                await tdata.edit(f"`It's`  **{dt.now().strftime(t_form)}**  `here.`")
                return

            time_zone = await get_tz(COUNTRY)
            await tdata.edit(
                f"`It's`  **{dt.now(time_zone).strftime(t_form)}**  `here, in {COUNTRY}`"
            )
            return

        time_zone = await get_tz(con)
        if not time_zone:
            await tdata.edit("``` Wrong country given! Try again! ```")
            return

        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con

        await tdata.edit(f"`It's`  **{dt.now(time_zone).strftime(t_form)}**  `in {c_name}`")

@register(outgoing=True, pattern="^.date ?(.*)")
async def date_func(dat):
    """ For .date command, return the date of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .ctime),
        3. The server where the userbot runs.
    """
    if not dat.text[0].isalpha() and dat.text[0] not in ("/", "#", "@", "!"):
        d_form = "%d/%m/%y - %A"
        con = dat.pattern_match.group(1)

        if not con:
            if not COUNTRY:
                await dat.edit(f"`It's`  **{dt.now().strftime(d_form)}**  `here.`")
                return

            time_zone = await get_tz(COUNTRY)
            await dat.edit(
                f"`It's`  **{dt.now(time_zone).strftime(d_form)}**  `here, in {COUNTRY}.`"
            )
            return

        time_zone = await get_tz(con)
        if not time_zone:
            await dat.edit("``` Wrong country given! Try again! ```")
            return

        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con

        await dat.edit(f"`It's`  **{dt.now().strftime(d_form)}**  `in {c_name}`")

@register(outgoing=True, pattern="^.ctime (.*)")
async def set_time_country(loc):
    """ For .ctime command, change the default userbot country for date and time commands. """
    if not loc.text[0].isalpha() and loc.text[0] not in ("/", "#", "@", "!"):
        global COUNTRY
        temp_country = loc.pattern_match.group(1)

        time_zone = await get_tz(temp_country)
        if not time_zone:
            await loc.edit("``` Wrong country given! Try again! ```")
            return
        
        try:
            c_name = c_n[temp_country]
        except KeyError:
            c_name = temp_country

        COUNTRY = c_name

        await loc.edit(f"``` Default country for date and time set to {COUNTRY} successfully! ```")

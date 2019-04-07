# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for getting the weather of a city. """

import json
import requests
from datetime import datetime
from pytz import country_timezones as c_tz, timezone as tz, country_names as c_n

from userbot import OPEN_WEATHER_MAP_APPID as OWM_API, HELPER
from userbot.events import register


#===== CONSTANT =====
DEFCITY = ''
#====================


async def get_tz(con):
    """ Get time zone of the given country. """
    """ Credits: @aragon12 and @zakaryan2004. """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@register(outgoing=True, pattern="^.weather ?(.*)")
async def get_weather(weather):
    """ For .weather command, gets the current weather of a city. """
    if not weather.text.startswith("."):
        return

    if len(OWM_API) < 1:
        await weather.edit("Get an API key from https://openweathermap.org/ first.")
        return
    
    APPID = OWM_API

    if not weather.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await weather.edit("Please specify a city or set one as default.")
            return
    else:
        CITY = weather.pattern_match.group(1)

    timezone_countries = {timezone: country 
                      for country, timezones in c_tz.items()
                      for timezone in timezones}

    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await weather.edit("Invalid country.")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
    request = requests.get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await weather.edit(f"{result['message']}")
        return

    cityname = result['name']
    curtemp = result['main']['temp']
    humidity = result['main']['humidity']
    min_temp = result['main']['temp_min']
    max_temp = result['main']['temp_max']
    desc = result['weather'][0]
    desc = desc['main']
    country = result['sys']['country']
    sunrise = result['sys']['sunrise']
    sunset = result['sys']['sunset']
    wind = result['wind']['speed']

    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%I:%M %p")
    day = datetime.now(ctimezone).strftime("%A")
    fullc_n = c_n[f"{country}"]

    fahrenheit = str(((curtemp - 273.15) * 9/5 + 32)).split(".")
    celsius =  str((curtemp - 273.15)).split(".")

    await weather.edit(f"**Temperature:** {celsius[0]}°C / {fahrenheit[0]}°F\n"
        +f"**Humidity:** {humidity}%\n"
        +f"**Wind:** {wind} m/s\n\n\n"
        +f"**{desc}**\n"
        +f"`{cityname}, {fullc_n}`\n"
        +f"`{day}, {time}`")

@register(outgoing=True, pattern="^.setcity ?(.*)")
async def set_default_city(city):
    """ For .ctime command, change the default userbot country for date and time commands. """
    if not city.text.startswith("."):
        return

    if len(OWM_API) < 1:
        await city.edit("Get an API key from https://openweathermap.org/ first.")
        return
    
    global DEFCITY
    APPID = OWM_API

    if not city.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await city.edit("Please specify a city to set one as default.")
            return
    else:
        CITY = city.pattern_match.group(1)

    timezone_countries = {timezone: country 
                      for country, timezones in c_tz.items()
                      for timezone in timezones}

    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await city.edit("Invalid country.")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()        

    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
    request = requests.get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await city.edit(f"{result['message']}")
        return

    DEFCITY = CITY
    cityname = result['name']
    country = result['sys']['country']

    fullc_n = c_n[f"{country}"]

    await city.edit(f"Set default city as {cityname}, {fullc_n}.")


HELPER.update({
    "weather": ".weather <city> or .weather <city>, <country name/code>\
    \nUsage: Gets the weather of a city.\n\
    \n.setcity <city> or .setcity <city>, <country name/code>\
    \nUsage: Sets your default city so you can just use .weather."
})

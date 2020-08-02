import json
from datetime import datetime

from pytz import (country_timezones as c_tz,
                  timezone as tz, country_names as c_n)
from requests import get

from userbot import (OPEN_WEATHER_MAP_APPID as OWM_API,
                     OPEN_WEATHER_MAP_DEFCITY as DEFCITY, CMD_HELP)
from userbot.events import register


async def get_tz(con):
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@register(outgoing=True, pattern="^.weather(?: |$)(.*)")
async def get_weather(weather):
    if not weather.text[0].isalpha() and weather.text[0] in ("."):
        if not OWM_API:
            await weather.edit("`Get an API key from` https://openweathermap.org/ `first.`")
            return
        APPID = OWM_API
        result = None
        if not weather.pattern_match.group(1):
            CITY = DEFCITY
            if not CITY:
                await weather.edit("`Please specify a city or set one as default.`")
                return
        else:
            CITY = weather.pattern_match.group(1)
        timezone_countries = {
            timezone: country
            for country, timezones in c_tz.items() for timezone in timezones
        }
        if "," in CITY:
            newcity = CITY.split(",")
            if len(newcity[1]) == 2:
                CITY = newcity[0].strip() + "," + newcity[1].strip()
            else:
                country = await get_tz((newcity[1].strip()).title())
                try:
                    countrycode = timezone_countries[f'{country}']
                except KeyError:
                    await weather.edit("`Invalid country.`")
                    return
                CITY = newcity[0].strip() + "," + countrycode.strip()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}'
        request = get(url)
        result = json.loads(request.text)
        if request.status_code != 200:
            await weather.edit(f"`Invalid country.`")
            return

        cityname = result['name']
        curtemp = result['main']['temp']
        humidity = result['main']['humidity']
        min_temp = result['main']['temp_min']
        max_temp = result['main']['temp_max']
        country = result['sys']['country']
        sunrise = result['sys']['sunrise']
        sunset = result['sys']['sunset']
        wind = result['wind']['speed']
        weath = result['weather'][0]
        desc = weath['main']
        icon = weath['id']
        condmain = weath['main']
        conddet = weath['description']

        if icon <= 232:  # Rain storm
            icon = "⛈"
        elif icon <= 321:  # Drizzle
            icon = "🌧"
        elif icon <= 504:  # Light rain
            icon = "🌦"
        elif icon <= 531:  # Cloudy rain
            icon = "⛈"
        elif icon <= 622:  # Snow
            icon = "❄️"
        elif icon <= 781:  # Atmosphere
            icon = "🌪"
        elif icon <= 800:  # Bright
            icon = "☀️"
        elif icon <= 801:  # A little cloudy
            icon = "⛅️"
        elif icon <= 804:  # Cloudy
            icon = "☁️"

        ctimezone = tz(c_tz[country][0])
        time = datetime.now(ctimezone).strftime(
            "%A %d %b, %H:%M").lstrip("0").replace(" 0", " ")
        fullc_n = c_n[f"{country}"]
        dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        kmph = str(wind * 3.6).split(".")
        mph = str(wind * 2.237).split(".")

        def fahrenheit(f):
            temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
            return temp[0]

        def celsius(c):
            temp = str((c - 273.15)).split(".")
            return temp[0]

        def sun(unix):
            xx = datetime.fromtimestamp(unix, tz=ctimezone).strftime(
                "%H:%M").lstrip("0").replace(" 0", " ")
            return xx

        await weather.edit(
            f"**{cityname}, {fullc_n}**\n"
            +
            f"`{time}`\n\n"
            +
            f"**Temperature:** `{celsius(curtemp)}°C\n`"
            +
            f"**Condition:** `{condmain}, {conddet}` " + f"{icon}\n"
            +
            f"**Humidity:** `{humidity}%`\n"
            +
            f"**Wind:** `{kmph[0]} km/h`\n"
            +
            f"**Sunrise**: `{sun(sunrise)}`\n"
            +
            f"**Sunset**: `{sun(sunset)}`")


CMD_HELP.update({"weather": ["Weather",
                             " - `weather` <city> or weather <city>, <country name/code>: "
                             "Gets the weather of a city.\n\n"
                             "**All commands can be used with** `.`"]})

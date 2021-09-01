from covid import Covid

from userbot.utils import admin_cmd

from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="corona (.*)"))

async def _(event):

    covid = Covid()

    data = covid.get_data()

    country = event.pattern_match.group(1)

    country_data = get_country_data(country, data)

    output_text = "" 

    for name, value in country_data.items():

        output_text += "`{}`: `{}`\n".format(str(name), str(value))

    await event.edit("**CoronaVirus Info in {}**:\n\n{}".format(country.capitalize(), output_text))

def get_country_data(country, world):

    for country_data in world:

        if country_data["country"].lower() == country.lower():

            return country_data

    return {"Status": "No information yet about this country!"}

CMD_HELP.update(

    {

        "corona": ".corona (country name)"

    }

)


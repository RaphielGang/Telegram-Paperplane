from pokedex import pokedex as dex

from userbot.events import register, grp_exclude

@register(outgoing=True, pattern="pokedex")
@grp_exclude()
async def pokedex(dexter):
    pokedex = dex.Pokedex(version = 'v1')
    pokemon_name = str(dexter.text[9: ])
    pokemon = pokedex.get_pokemon_by_name(pokemon_name)
    await dexter.edit(str(pokemon))

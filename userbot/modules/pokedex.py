from pokedex import pokedex as pokedex

from userbot.events import register, grp_exclude

@register(outgoing=True, pattern="pokedex")
@grp_exclude()
async def pokedex(pallet):
    pokedex = pokedex.Pokedex(version = 'v1')
    pokemon_name = str(pallet.text[9: ])
    pokemon = pokedex.get_pokemon_by_name(pokemon_name)
    await pallet.edit(str(pokemon))

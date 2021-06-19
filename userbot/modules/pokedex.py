import pypokedex

from userbot.events import register, grp_exclude

@register(outgoing=True, pattern="pokedex")
@grp_exclude()
async def pokedex(pallet):
    pokemon_name = str(pallet.text[9: ])
    pokemon = pypokedex.get(name=pokemon_name)
    await pallet.edit(str(pokemon.types))

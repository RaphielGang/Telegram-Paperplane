import pypokedex

from userbot import register, grp_exclude

@register(outgoing=True, pattern="pokedex")
@grp_exclude()
async def pokedex(pallet):
    pokemon_name = str(pallet.text[8: ])
    pokemon = pypokedex.get(name=pokemon_name)
    await pallet.edit(pokemon.types)

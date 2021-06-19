import pypokedex as dex

from userbot.events import register, grp_exclude

@register(outgoing=True, pattern="pokedex")
@grp_exclude()
async def pokedex(dexter):
    pokemon_name = str(dexter.text[9: ])
    pokemon = dex.get(name=pokemon_name)

 
  #================= POKEMON STATS ================= #   
    Name = str(pokemon.name)                         #
    Height = str(pokemon.height)                     #
    Weight = str(pokemon.weight)                     #
    Exp = str(pokemon.base_experience)               #                   
    Ability = str(pokemon.abilities(name))           #
                                                     #
                                                     #
                                                     #
                                                     #
                                                     #
                                                     #
                                                     #
  #================================================= #
  
    message = (
        f"**Name: **{Name}\n"
        f"**Type: **{Type}\n"
        f"**Abilities: **{Ability}\n"
       #f"**Gender: **{Gender}"
        f"**Height: **{Height}\n"
        f"**Weight: **{Weight}\n"
       #f"**Stage: **{Stage}"
       #f"**Evolution: **{Evolution}"
       #f"**EggGroup: **{EggGroup}"
       #f"**Description: **__{Description}__"
    )

    await dexter.edit(message)

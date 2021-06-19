from pokedex import pokedex as dex

from userbot.events import register, grp_exclude

@register(outgoing=True, pattern="pokedex")
@grp_exclude()
async def pokedex(dexter):
    pokedex = dex.Pokedex(version = 'v1')
    pokemon_name = str(dexter.text[9: ])
    pokemon = pokedex.get_pokemon_by_name(pokemon_name)
    pokedetails = str(pokemon)
    
  #================= POKEMON STATS ==================== #   
    Name = pokedetails['name']                          #
    Species = pokedetails['species']                    #
    Type = pokedetails['types']                         #
    Ability = pokedetails['abilities']                  #                   
    EggGroup = pokedetails['eggGroups']['normal']       #
    Stage = pokedetails['family']['evolutionStage']     #
    Evolution = pokedetails['family']['evolutionLine']  #
    Gender = pokedetails['gender']                      #
    Height = pokedetails['height']                      #
    Weight = pokedetails['weight']                      #
    Sprite = pokedetails['sprite']                      #
    Description = pokedetails['description']            #
  #==================================================== #
  
    message = (
        f"**Name: **{Name}"
        f"**Type: **{Type}"
        f"**Abilities: **{Ability}"
        f"**Gender: **{Gender}"
        f"**Height: **{Height}"
        f"**Weight: **{Weight}"
        f"**Stage: **{Stage}"
        f"**Evolution: **{Evolution}"
        f"**EggGroup: **{EggGroup}"
        f"**Description: **__{Description}__"
    )
    
    await dexter.reply(message)

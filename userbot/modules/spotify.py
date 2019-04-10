import requests, json, time
from telethon.tl.functions.account import UpdateProfileRequest
from userbot import bot, HELPER, DEFAULT_BIO, SPOTIFY_AUTH_KEY, SPOTIFY_BIO_PREFIX
from userbot.events import register

SPO_BIO_ENABLED = "```Spotify Current Music to Bio Enabled.```"
SPO_BIO_DISABLED = "```Spotify Current Music to Bio Disabled.```"
SPO_BIO_RUNNING = "```Spotify Current Music to Bio already running.```"
SPO_BIO_CONFIG_ERROR = "```Error.```"


auth_token = SPOTIFY_AUTH_KEY
hed = {'Authorization': 'Bearer ' + auth_token}
url = 'https://api.spotify.com/v1/me/player/currently-playing'

artist = 0
song = 0

bioprefix = SPOTIFY_BIO_PREFIX

spotifycheck = False
running = False

async def update_spotify_info():
  global data,response,running,artist,song
  while spotifycheck:
    try:
      running = True
      response = requests.get(url, headers=hed)
      data = json.loads(response.content)
      artist = data['item']['album']['artists'][0]['name']
      song = data['item']['name']
      spobio = bioprefix + " 🎧: " + artist + " - " + song
      print(spobio)
      await bot(UpdateProfileRequest(about=spobio))
      time.sleep(60)
    except KeyError:
      time.sleep(15)
      await bot(UpdateProfileRequest(about=DEFAULT_BIO))
      print ("There isn't any song currently playing. Reverting back to default bio.")
    except json.decoder.JSONDecodeError:
      time.sleep(15)
      await bot(UpdateProfileRequest(about=DEFAULT_BIO))
      print ("There isn't any song currently playing. Reverting back to default bio.")
  running = False


@register(outgoing=True, pattern="^.enablespotify")
async def set_biostgraph(setstbio):
	global spotifycheck
	spotifycheck = True
	if not running:
		await setstbio.edit(SPO_BIO_ENABLED)
		await update_spotify_info()
	else:
		await setstbio.edit(SPO_BIO_RUNNING)

@register(outgoing=True, pattern="^.disablespotify")
async def set_biodgraph(setdbio):
	global spotifycheck
	spotifycheck = False
	await setdbio.edit(SPO_BIO_DISABLED)
import requests, json, time, os, asyncio, sys
import spotify_token as st
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from userbot import bot, HELPER, DEFAULT_BIO, SPOTIFY_USERNAME, SPOTIFY_PASS, SPOTIFY_BIO_PREFIX, LOGGER, LOGGER_GROUP
from userbot.events import register

SPO_BIO_ENABLED = "```Spotify Current Music to Bio enabled.```"
SPO_BIO_DISABLED = "```Spotify Current Music to Bio disabled. Bio is default now.```"
SPO_BIO_RUNNING = "```Spotify Current Music to Bio already running.```"
SPO_BIO_CONFIG_ERROR = "```Error.```"

username = SPOTIFY_USERNAME
passw = SPOTIFY_PASS

artist = 0
song = 0

bioprefix = SPOTIFY_BIO_PREFIX

spotifycheck = False
running = False
oldexcept = False
parse = False

async def get_spotify_token():
	global access_token,sptoken
	sptoken = st.start_session(username,passw)
	access_token = sptoken[0]
	expiration_date = sptoken[1]
	os.environ["spftoken"] = access_token

async def update_spotify_info():
	global data,response,running,artist,song,oldexcept,oldartist,oldsong,parse,spotifycheck
	oldartist = ""
	oldsong = ""
	while spotifycheck:
		try:
			running = True
			spftoken = os.environ.get("spftoken", None)
			hed = {'Authorization': 'Bearer ' + spftoken}
			url = 'https://api.spotify.com/v1/me/player/currently-playing'
			response = requests.get(url, headers=hed)
			data = json.loads(response.content)
			artist = data['item']['album']['artists'][0]['name']
			song = data['item']['name']
			oldexcept = False
			oldsong = os.environ.get("oldsong", None)
			if song != oldsong and artist != oldartist:
				oldartist = artist
				os.environ["oldsong"] = song
				spobio = bioprefix + " 🎧: " + artist + " - " + song
				await bot(UpdateProfileRequest(about=spobio))
				os.environ["errorcheck"] = "0"
		except KeyError:
			errorcheck = os.environ.get("errorcheck", None)
			if errorcheck == 0:
				await update_token()
			elif errorcheck == 1:
				spotifycheck = False
				await bot(UpdateProfileRequest(about=DEFAULT_BIO))
				print ("Either you paused music or got unexcepted error. Spotify Music to Bio module stopped now.")
				if LOGGER:
					await bot.send_message(LOGGER_GROUP, "Either you paused music or got unexcepted error. Spotify Music to Bio module stopped now.")
		except json.decoder.JSONDecodeError:
			oldexcept = True
			await asyncio.sleep(6)
			await bot(UpdateProfileRequest(about=DEFAULT_BIO))
		except TypeError:
			await dirtyfix()
		spotifycheck = False
		await asyncio.sleep(2)
		await dirtyfix()
	running = False


async def update_token():
	global access_token,sptoken
	sptoken = st.start_session(username,passw)
	access_token = sptoken[0]
	expiration_date = sptoken[1]
	os.environ["spftoken"] = access_token
	os.environ["errorcheck"] = "1"
	await update_spotify_info()

async def dirtyfix():
	global spotifycheck
	spotifycheck = True
	await asyncio.sleep(4)
	await update_spotify_info()

@register(outgoing=True, pattern="^.enablespotify")
async def set_biostgraph(setstbio):
	sys.setrecursionlimit(700000)
	if not spotifycheck:
		os.environ["errorcheck"] = "0"
		await setstbio.edit(SPO_BIO_ENABLED)
		await get_spotify_token()
		await dirtyfix()
	else:
		await setstbio.edit(SPO_BIO_RUNNING)

@register(outgoing=True, pattern="^.disablespotify")
async def set_biodgraph(setdbio):
	global spotifycheck,running
	spotifycheck = False
	running = False
	await bot(UpdateProfileRequest(about=DEFAULT_BIO))
	await setdbio.edit(SPO_BIO_DISABLED)

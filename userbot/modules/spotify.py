from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ
from sys import setrecursionlimit

import spotify_token as st
from requests import get
from telethon.errors import AboutTooLongError
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (DEFAULT_BIO, CMD_HELP, BOTLOG, BOTLOG_CHATID, BIO_PREFIX,
                     SPOTIFY_PASS, SPOTIFY_USERNAME, bot)
from userbot.events import register, errors_handler

# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify current music to bio is now enabled.`"
SPO_BIO_DISABLED = "`Spotify current music to bio is now disabled. "
SPO_BIO_DISABLED += "Bio reverted to default.`"
SPO_BIO_RUNNING = "`Spotify current music to bio is already running.`"
ERROR_MSG = "`Spotify module halted, got an unexpected error.`"

USERNAME = SPOTIFY_USERNAME
PASSWORD = SPOTIFY_PASS

ARTIST = 0
SONG = 0

BIOPREFIX = BIO_PREFIX

SPOTIFYCHECK = False
RUNNING = False
OLDEXCEPT = False
PARSE = False


# ================================================
async def get_spotify_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    global ARTIST
    global SONG
    global PARSE
    global SPOTIFYCHECK
    global RUNNING
    global OLDEXCEPT
    oldartist = ""
    oldsong = ""
    while SPOTIFYCHECK:
        try:
            RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data['item']['album']['artists'][0]['name']
            song = data['item']['name']
            OLDEXCEPT = False
            oldsong = environ.get("oldsong", None)
            if song != oldsong and artist != oldartist:
                oldartist = artist
                environ["oldsong"] = song
                spobio = BIOPREFIX + " 🎧: " + artist + " - " + song
                try:
                    await bot(UpdateProfileRequest(about=spobio))
                except AboutTooLongError:
                    short_bio = "🎧: " + song
                    await bot(UpdateProfileRequest(about=short_bio))
                environ["errorcheck"] = "0"
        except KeyError:
            errorcheck = environ.get("errorcheck", None)
            if errorcheck == 0:
                await update_token()
            elif errorcheck == 1:
                SPOTIFYCHECK = False
                await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                print(ERROR_MSG)
                if BOTLOG:
                    await bot.send_message(BOTLOG_CHATID, ERROR_MSG)
        except JSONDecodeError:
            OLDEXCEPT = True
            await sleep(6)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
        except TypeError:
            await dirtyfix()
        SPOTIFYCHECK = False
        await sleep(2)
        await dirtyfix()
    RUNNING = False


async def update_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    environ["errorcheck"] = "1"
    await update_spotify_info()


async def dirtyfix():
    global SPOTIFYCHECK
    SPOTIFYCHECK = True
    await sleep(4)
    await update_spotify_info()


@register(outgoing=True, pattern="^.enablespotify$")
@errors_handler
async def set_biostgraph(setstbio):
    setrecursionlimit(700000)
    if not SPOTIFYCHECK:
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.disablespotify$")
@errors_handler
async def set_biodgraph(setdbio):
    global SPOTIFYCHECK
    global RUNNING
    SPOTIFYCHECK = False
    RUNNING = False
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)


CMD_HELP.update({"enablespotify": "Usage: Enable Spotify bio updating."})

CMD_HELP.update({"disablespotify": "Usage: Disable Spotify bio updating."})

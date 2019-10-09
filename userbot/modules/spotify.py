# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting currently playing Spotify music. """

from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ
from sys import setrecursionlimit

import spotify_token as st
from requests import get
from telethon.errors import AboutTooLongError
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     SPOTIFY_PASS, SPOTIFY_USERNAME, bot, is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import (exceptionexist, getspotifycheck,
                                      sfgetartist, sfgetsong, sfsetartist,
                                      sfsetsong, spotifycheck)

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
# ================================================
async def get_spotify_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():
    oldartist = ""
    oldsong = ""
    while await getspotifycheck():
        try:
            spftoken = environ.get("spftoken", None)
            hed = {'Authorization': 'Bearer ' + spftoken}
            url = 'https://api.spotify.com/v1/me/player/currently-playing'
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data['item']['album']['artists'][0]['name']
            await sfsetartist(artist)
            song = data['item']['name']
            await sfsetsong(song)
            await exceptionexist("False")
            oldsong = environ.get("oldsong", None)
            if song != oldsong and artist != oldartist:
                oldartist = artist
                environ["oldsong"] = await sfgetsong()
                spobio = f"{BIOPREFIX} 🎧: {await sfgetartist()} - {await sfgetsong()}"
                try:
                    await bot(UpdateProfileRequest(about=spobio))
                except AboutTooLongError:
                    short_bio = f"🎧: {await sfgetsong()}"
                    await bot(UpdateProfileRequest(about=short_bio))
                environ["errorcheck"] = "0"
        except KeyError:
            errorcheck = environ.get("errorcheck", None)
            if errorcheck == 0:
                await update_token()
            elif errorcheck == 1:
                await spotifycheck("False")
                await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                print(ERROR_MSG)
                if BOTLOG:
                    await bot.send_message(BOTLOG_CHATID, ERROR_MSG)
        except JSONDecodeError:
            await exceptionexist(True)
            await sleep(6)
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
        except TypeError:
            await dirtyfix()
        await spotifycheck("False")
        await sleep(2)
        await dirtyfix()


async def update_token():
    sptoken = st.start_session(USERNAME, PASSWORD)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    environ["errorcheck"] = "1"
    await update_spotify_info()


async def dirtyfix():
    await spotifycheck("True")
    await sleep(4)
    await update_spotify_info()


@register(outgoing=True, pattern="^.enablespotify$")
async def set_biostgraph(setstbio):
    if not is_redis_alive():
        setstbio.edit("Who forgot their Redis?")
        return
    setrecursionlimit(700000)
    if await getspotifycheck() == "True":
        environ["errorcheck"] = "0"
        await setstbio.edit(SPO_BIO_ENABLED)
        await get_spotify_token()
        await dirtyfix()
    else:
        await setstbio.edit(SPO_BIO_RUNNING)


@register(outgoing=True, pattern="^.disablespotify$")
async def set_biodgraph(setdbio):
    if not is_redis_alive():
        setdbio.edit("Who forgot their Redis?")
        return
    await spotifycheck("False")
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await setdbio.edit(SPO_BIO_DISABLED)


CMD_HELP.update({"enablespotify": "Usage: Enable Spotify bio updating."})

CMD_HELP.update({"disablespotify": "Usage: Disable Spotify bio updating."})

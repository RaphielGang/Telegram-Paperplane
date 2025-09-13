# Copyright (C) 2019-2025 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import os
import re
import requests
from datetime import timedelta

from telethon.tl.functions.account import UpdateProfileRequest
from telethon import functions, types

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    SPOTIPY_CLIENT,
    bot,
)
from userbot.events import register, grp_exclude, log_error
from userbot.modules.dbhelper import (
    get_music_config,
    set_spotify_bio,
    set_music_name_emoji,
)


# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify Currently Listening in Profile is now enabled.`"
SPO_BIO_DISABLED = (
    "`Spotify Currently Listening in Profile is now disabled.`"
)
SPO_DISABLED = "`Spotify module is disabled! Make sure you have set up the environment variables properly.`"
# ================================================


CACHED_SONG_FILES = {}
CURRENT_INFO = {}


def reset_current_info():
    global CURRENT_INFO
    CURRENT_INFO = {
        "playing": False,
        "song": "",
        "artists": [],
        "song_url": "",
        "preview_url": None,
        "music_sent_file": None
    }

reset_current_info()


async def save_music_to_profile(music_message, unsave=False):
    if not music_message or not isinstance(music_message, types.Message):
        return None

    music = music_message.media.document
    input_doc = types.InputDocument(
        id=music.id,
        access_hash=music.access_hash,
        file_reference=music.file_reference,
    )

    await bot(functions.account.SaveMusicRequest(id=input_doc, unsave=unsave))
    return input_doc.id


async def download_music_preview(preview_url, cover_art, song, artists):
    if not preview_url:
        return None
    
    chat_id = BOTLOG_CHATID if BOTLOG and BOTLOG_CHATID else "me"
    if preview_url in CACHED_SONG_FILES:
        try:
            return await bot.get_messages(chat_id, ids=CACHED_SONG_FILES[preview_url])
        except Exception:
            pass

    # Download the preview audio
    audio_data = requests.get(preview_url).content
    with open("preview.mp3", "wb") as f:
        f.write(audio_data)
    
    # Download cover art
    cover_data = requests.get(cover_art).content
    with open("cover.jpg", "wb") as f:
        f.write(cover_data)

    sent_message = await bot.send_file(
        chat_id,
        "preview.mp3",
        thumb="cover.jpg",
        attributes=[
            types.DocumentAttributeAudio(
                duration=30,
                title=f"[paperplane] {song}",
                performer=artists
            )
        ]
    )

    # Clean up
    os.remove("preview.mp3")
    os.remove("cover.jpg")

    CACHED_SONG_FILES[preview_url] = sent_message.id

    return sent_message


async def update_spotify_info(trigger_one=False):
    global CURRENT_INFO
    if not SPOTIPY_CLIENT:
        return

    is_playing = False
    triggered = False

    while not triggered and (music_config := await get_music_config() or {}).get(
        "spotify_bio", False
    ):
        if trigger_one:
            triggered = True
        try:
            name_emoji_enabled = music_config.get("name_emoji", False)
            user = await bot.get_me()
            default_name = (
                re.sub(r"🎧$", r"", user.last_name or '')
                if name_emoji_enabled
                else user.last_name or ''
            )

            data = SPOTIPY_CLIENT.current_playback()

            if not data:
                if is_playing:
                    await bot(UpdateProfileRequest(last_name=default_name))
                    is_playing = False

                    # Unsave old music if exists
                    await save_music_to_profile(CURRENT_INFO['music_sent_file'], unsave=music_config.get('keep_old_music', False) is False)
                    reset_current_info()
                await asyncio.sleep(15)
                continue

            is_playing = data["is_playing"]
            if is_playing:
                if data["currently_playing_type"] != "track":
                    await asyncio.sleep(15)
                    continue

                if data['item']['external_urls']['spotify'] == CURRENT_INFO['song_url']:
                    await asyncio.sleep(15)
                    continue

                # Unsave old music if exists
                await save_music_to_profile(CURRENT_INFO['music_sent_file'], unsave=music_config.get('keep_old_music', False) is False)

                artists_array = [artist for artist in data["item"]["artists"]]
                artists = ", ".join([artist["name"] for artist in artists_array])
                song = data["item"]["name"]
                cover_art = data['item']['album']['images'][0]['url']

                song_page = requests.get(data['item']['external_urls']['spotify']).text
                preview_urls = re.findall(r'https://p\.scdn\.co/mp3-preview/[a-zA-Z0-9]+', song_page)

                CURRENT_INFO = {
                    "playing": True,
                    "song": song,
                    "artists": artists_array,
                    "song_url": data['item']['external_urls']['spotify'],
                    "preview_url": preview_urls[0] if preview_urls else None,
                    "music_sent_file": None
                }

                # Download preview URL and cover art and send as audio file if available
                if CURRENT_INFO['preview_url']:
                    CURRENT_INFO['music_sent_file'] = await download_music_preview(
                        CURRENT_INFO['preview_url'], cover_art, song, artists
                    )

                    CURRENT_INFO['profile_music_id'] = await save_music_to_profile(CURRENT_INFO['music_sent_file'], unsave=False)
            else:
                await bot(UpdateProfileRequest(last_name=default_name))

                is_playing = False

                # Unsave old music if exists
                await save_music_to_profile(CURRENT_INFO['music_sent_file'], unsave=music_config.get('keep_old_music', False) is False)
                reset_current_info()
            await asyncio.sleep(15)
        except Exception as e:
            await log_error(error=e, event=None)
            await asyncio.sleep(15)
            continue


if SPOTIPY_CLIENT:
    bot.loop.create_task(update_spotify_info(), name="spotify")


@register(outgoing=True, pattern=r"^.spotifybio (on|off)$")
@grp_exclude()
async def set_biostgraph(setstbio):
    if not SPOTIPY_CLIENT:
        await setstbio.edit(SPO_DISABLED)
        return

    newstate = True if setstbio.pattern_match.group(1) == "on" else False
    await set_spotify_bio(newstate)

    if newstate:
        if not [task for task in asyncio.all_tasks() if task.get_name() == "spotify"]:
            bot.loop.create_task(update_spotify_info(), name="spotify")
    else:
        music_config = await get_music_config() or {}
        if music_config.get("name_emoji", False):
            user = await bot.get_me()
            default_name = re.sub(r"🎧$", r"", user.last_name or '')
            await bot(UpdateProfileRequest(last_name=default_name))

    await setstbio.edit(SPO_BIO_ENABLED if newstate else SPO_BIO_DISABLED)
    if BOTLOG:
        await setstbio.client.send_message(
            BOTLOG_CHATID, SPO_BIO_ENABLED if newstate else SPO_BIO_DISABLED
        )


@register(outgoing=True, pattern=r"^.myspotify$")
@grp_exclude()
async def get_curr_song_spotify(getstbio):
    if not SPOTIPY_CLIENT:
        await getstbio.edit(SPO_DISABLED)
        return

    music_config = await get_music_config() or {}
    if not music_config.get("spotify_bio"):
        await getstbio.edit(SPO_BIO_DISABLED)
        return

    await getstbio.edit("`Fetching the current track...`")

    data = SPOTIPY_CLIENT.current_playback()

    if not data:
        await getstbio.edit("`No music is playing right now on my Spotify.`")
        return

    artists = ", ".join(
        [
            f"<b><a href='{artist['external_urls']['spotify']}'>{artist['name']}</a></b>"
            for artist in data["item"]["artists"]
        ]
    )
    song = f"<b><a href='{data['item']['external_urls']['spotify']}'>{data['item']['name']}</a></b>"
    album = f"<b><a href='{data['item']['album']['external_urls']['spotify']}'>{data['item']['album']['name']}</a></b>"
    on_repeat = "<b> on repeat</b>" if data["repeat_state"] == "track" else ""
    paused = "<b> (Paused)</b>" if not data["is_playing"] else ""
    song_page = requests.get(data['item']['external_urls']['spotify']).text
    preview_urls = re.findall(r'https://p\.scdn\.co/mp3-preview/[a-zA-Z0-9]+', song_page)

    message = (
        f"<b>🎧 Spotify Current Track</b>\n\n"
        f"I am currently listening to {song} by {artists}{on_repeat}{paused}"
        f"\n\nThis song is from the album {album}"
        f"\n\n<b>Preview URL(s):</b> {', '.join(preview_urls) if preview_urls else 'Not available'}"
    )

    await getstbio.edit(message, parse_mode="html")

    await update_spotify_info(trigger_one=True)


@register(outgoing=True, pattern=r"^.spotifylink ?(.*)?$")
@grp_exclude()
async def spotify_search(stsearch):
    if not SPOTIPY_CLIENT:
        await stsearch.edit(SPO_DISABLED)
        return

    track = stsearch.pattern_match.group(1)
    reply = await stsearch.get_reply_message()

    if track:
        pass
    elif reply.text:
        match_url = re.search(r"open.spotify.com/track/(\w+)", reply.text)
        match_uri = re.search(r"spotify:track:(\w+)", reply.text)
        if match_url:
            track = match_url.group(1)
        elif match_uri:
            track = match_uri.group(1)
        else:
            await stsearch.edit("`Invalid Spotify track link/URI!`")
            return
    else:
        await stsearch.edit(
            "`Either reply to a message containing a Spotify link or pass it as an argument!`"
        )
        return

    await stsearch.edit("`Fetching the song...`")

    try:
        trackdata = SPOTIPY_CLIENT.track(track)

        artists = ", ".join(
            [
                f"[{artist['name']}]({artist['external_urls']['spotify']})"
                for artist in trackdata["artists"]
            ]
        )
        song = f"[{trackdata['name']}]({trackdata['external_urls']['spotify']})"
        album = f"[{trackdata['album']['name']}]({trackdata['album']['external_urls']['spotify']})"
        song_page = requests.get(trackdata['external_urls']['spotify']).text
        preview_urls = re.findall(r'https://p\.scdn\.co/mp3-preview/[a-zA-Z0-9]+', song_page)
        message = (
            "**🎧 Spotify Song Details**\n\n"
            f"**Song:** {song}\n"
            f"**Artist(s):** {artists}\n"
            f"**Album:** {album}\n"
            f"**Duration:** `{':'.join(str(timedelta(seconds=int(trackdata['duration_ms'] / 1000))).split(':')[1:3])}`\n"
            f"**Link:** {trackdata['external_urls']['spotify']}\n"
            f"**Preview URL(s):** {', '.join(preview_urls) if preview_urls else 'Not available'}"
        )

        await stsearch.edit(message)
    except Exception as e:
        await stsearch.edit(f"`Invalid Spotify track link/URI!`")
        await log_error(error=e, event=stsearch)
        return


@register(outgoing=True, pattern=r"^.spotifysettings$")
@grp_exclude()
async def spotifysettings(settings):
    if not SPOTIPY_CLIENT:
        await settings.edit(SPO_DISABLED)
        return

    music_config = await get_music_config() or {}

    await settings.edit(
        "`Spotify settings:`\n\n"
        f"**Spotify Bio**: `{music_config.get('spotify_bio', False)}`\n"
        f"**Bio Prefix:** `{music_config.get('bio_prefix') or 'None'}`\n"
        f"**Default Bio:** `{music_config.get('default_bio') or 'None'}`\n"
        f"**Music Name Emoji:** `{music_config.get('name_emoji', False)}`\n"
    )


@register(outgoing=True, pattern=r"^.musicnameemoji (on|off)$")
@grp_exclude()
async def musicname(musicnme):
    if not SPOTIPY_CLIENT:
        await musicnme.edit(SPO_DISABLED)
        return
    
    if musicnme.pattern_match.group(1) not in ["on", "off"]:
        await musicnme.edit("`Invalid argument! Use either 'on' or 'off'.`")
        return

    newstate = True if musicnme.pattern_match.group(1) == "on" else False

    currname = (await bot.get_me()).last_name or ''

    if len(currname) > 62 and newstate:
        await musicnme.edit(
            "`Your last name is too long! Make it shorter for the emoji to fit!`"
        )
        return

    if not newstate:
        await bot(UpdateProfileRequest(last_name=re.sub(r"🎧$", r"", currname)))

    if await set_music_name_emoji(newstate):
        await musicnme.edit(
            f"`Music Name Emoji set to {musicnme.pattern_match.group(1)}!`"
        )
        if BOTLOG:
            await musicnme.client.send_message(
                BOTLOG_CHATID,
                f"`Music Name Emoji set to {musicnme.pattern_match.group(1)}!`",
            )
    else:
        await musicnme.edit("`Failed to toggle Music Name Emoji!`")
        if BOTLOG:
            await musicnme.client.send_message(
                BOTLOG_CHATID, "`Failed to toggle Music Name Emoji!`"
            )


@register(outgoing=True, pattern=r"^.keepoldmusic (on|off)$")
@grp_exclude()
async def keepoldmusic(komusic):
    if not SPOTIPY_CLIENT:
        await komusic.edit(SPO_DISABLED)
        return
    
    if komusic.pattern_match.group(1) not in ["on", "off"]:
        await komusic.edit("`Invalid argument! Use either 'on' or 'off'.`")
        return

    newstate = True if komusic.pattern_match.group(1) == "on" else False

    music_config = await get_music_config() or {}
    music_config['keep_old_music'] = newstate
    await music_config.save()

    await komusic.edit(f"`Keep Old Music set to {komusic.pattern_match.group(1)}!`")
    if BOTLOG:
        await komusic.client.send_message(
            BOTLOG_CHATID,
            f"`Keep Old Music set to {komusic.pattern_match.group(1)}!`",
        )


CMD_HELP.update(
    {
        "spotify": [
            "Spotify",
            " - `.spotifybio <on/off>`: Enable Spotify Currently Listening in Profile.\n"
            " - `.myspotify`: Show the song you are currently listening to.\n"
            " - `.spotifylink <link>`: Fetch song details from the URL/URI passed as an argument or "
            "replied to. You can also reply to the response of `.myspotify` to get details about the "
            "song you are currently listening to.\n"
            " - `.musicnameemoji <on/off>`: Toggle Music Name Emoji. Last name must be no more than 62 characters.\n"
            " - `.keepoldmusic <on/off>`: Keep the previously sent music in your profile's Music Library. By default, Paperplane unsaves the previously sent music when a new song starts playing.\n"
            " - `.spotifysettings`: Show the current settings of the Spotify module.\n",
        ]
    }
)

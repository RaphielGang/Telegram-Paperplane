# Copyright (C) 2019-2022 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import re
from datetime import timedelta

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUserSelf

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
    set_default_bio,
    set_bio_prefix,
    set_music_name_emoji,
)


# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify Current Music to Bio is now enabled.`"
SPO_BIO_DISABLED = (
    "`Spotify Current Music to Bio is now disabled. Bio reverted to default.`"
)
SPO_DISABLED = "`Spotify module is disabled! Make sure you have set up the environment variables properly.`"
# ================================================


async def update_spotify_info(trigger_one=False):
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
            default_bio = music_config.get("default_bio", "")
            bio_prefix = music_config.get("bio_prefix", "")
            name_emoji_enabled = music_config.get("name_emoji", False)
            userfull = await bot(GetFullUserRequest(InputUserSelf()))
            user = userfull.user
            default_name = (
                re.sub(r"( 🎧)$", r"", user.last_name)
                if name_emoji_enabled
                else user.last_name
            )

            data = SPOTIPY_CLIENT.current_playback()

            if not data:
                if is_playing:
                    await bot(
                        UpdateProfileRequest(about=default_bio, last_name=default_name)
                    )
                    is_playing = False
                await asyncio.sleep(15)
                continue

            is_playing = data["is_playing"]
            if is_playing:
                if data["currently_playing_type"] != "track":
                    await asyncio.sleep(15)
                    continue

                artists = [artist for artist in data["item"]["artists"]]
                artists = ", ".join([artist["name"] for artist in artists])
                song = data["item"]["name"]

                newname = (
                    f"{user.last_name} 🎧"
                    if user.last_name[-2:] != " 🎧"
                    else user.last_name
                )
                newbio = f"{bio_prefix} 🎧 {artists} - {song}"
                if len(newbio) > 70:
                    newbio = f"{bio_prefix} 🎧 {song}"
                    if len(newbio) > 70:
                        newbio = f"🎧 {song}"
                        if len(newbio) > 70:
                            if len(newbio) > 72:
                                newbio = default_bio
                            else:
                                newbio = song
            else:
                newbio = default_bio
                newname = default_name

            currbio = userfull.about
            currname = user.last_name

            if newbio != currbio:
                await bot(UpdateProfileRequest(about=newbio))
            if name_emoji_enabled and newname != currname:
                await bot(UpdateProfileRequest(last_name=newname))
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
        default_bio = music_config.get("default_bio", "")
        await bot(UpdateProfileRequest(about=default_bio))

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

    message = (
        f"<b>🎧 Spotify Current Track</b>\n\n"
        f"I am currently listening to {song} by {artists}{on_repeat}{paused}"
        f"\n\nThis song is from the album {album}"
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
        message = (
            "**🎧 Spotify Song Details**\n\n"
            f"**Song:** {song}\n"
            f"**Artist(s):** {artists}\n"
            f"**Album:** {album}\n"
            f"**Duration:** `{':'.join(str(timedelta(seconds=int(trackdata['duration_ms'] / 1000))).split(':')[1:3])}`\n"
            f"**Link:** {trackdata['external_urls']['spotify']}"
        )

        await stsearch.edit(message)
    except Exception as e:
        await stsearch.edit(f"`Invalid Spotify track link/URI!`")
        await log_error(error=e, event=stsearch)
        return


@register(outgoing=True, pattern=r"^.setdefaultbio (.*)$")
@grp_exclude()
async def setdefaultbio(setbio):
    if not SPOTIPY_CLIENT:
        await setbio.edit(SPO_DISABLED)
        return

    newbio = setbio.pattern_match.group(1)

    if len(newbio) > 70:
        await setbio.edit("`Default bio must be no more than 70 characters.`")
        return

    if await set_default_bio(newbio):
        await setbio.edit(f"`Default bio set to:`\n{newbio}")
        if BOTLOG:
            await setbio.client.send_message(
                BOTLOG_CHATID, f"`Default bio set to:`\n{newbio}"
            )
    else:
        await setbio.edit("`Failed to set default bio!`")
        if BOTLOG:
            await setbio.client.send_message(
                BOTLOG_CHATID, "`Failed to set default bio!`"
            )


@register(outgoing=True, pattern=r"^.setbioprefix (.*)$")
@grp_exclude()
async def setbioprefix(setbio):
    if not SPOTIPY_CLIENT:
        await setbio.edit(SPO_DISABLED)
        return

    newbioprefix = setbio.pattern_match.group(1)

    if len(newbioprefix) > 50:
        await setbio.edit("`Bio prefix must be no more than 50 characters.`")
        return

    if await set_bio_prefix(newbioprefix):
        await setbio.edit(f"`Bio prefix set to:`\n{newbioprefix}")
        if BOTLOG:
            await setbio.client.send_message(
                BOTLOG_CHATID, f"`Bio prefix set to:`\n{newbioprefix}"
            )
    else:
        await setbio.edit("`Failed to set bio prefix!`")
        if BOTLOG:
            await setbio.client.send_message(
                BOTLOG_CHATID, "`Failed to set bio prefix!`"
            )


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

    newstate = True if musicnme.pattern_match.group(1) == "on" else False

    currname = (await bot(GetFullUserRequest(InputUserSelf()))).user.last_name

    if len(currname) > 62 and newstate:
        await musicnme.edit(
            "`Your last name is too long! Make it shorter for the emoji to fit!`"
        )
        return

    if not newstate:
        await bot(UpdateProfileRequest(last_name=re.sub(r"( 🎧)$", r"", currname)))

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


CMD_HELP.update(
    {
        "spotify": [
            "Spotify",
            " - `.spotifybio <on/off>`: Enable Spotify Current Music to Bio.\n"
            " - `.myspotify`: Show the song you are currently listening to.\n"
            " - `.spotifylink <link>`: Fetch song details from the URL/URI passed as an argument or "
            "replied to. You can also reply to the response of `.myspotify` to get details about the "
            "song you are currently listening to.\n"
            " - `.setdefaultbio <bio>`: Set the default Spotify bio. Must be no more than 70 characters.\n"
            " - `.setbioprefix <prefix>`: Set the bio prefix. Must be no more than 50 characters.\n"
            " - `.musicnameemoji <on/off>`: Toggle Music Name Emoji. Last name must be no more than 62 characters.\n"
            " - `.spotifysettings`: Show the current settings of the Spotify module.\n",
        ]
    }
)

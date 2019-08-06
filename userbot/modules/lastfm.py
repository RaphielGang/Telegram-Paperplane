from asyncio import sleep
from pylast import User
from re import sub
from urllib import parse
from os import environ
from sys import setrecursionlimit

from telethon.errors import AboutTooLongError
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import CMD_HELP, DEFAULT_BIO, BIO_PREFIX, lastfm, LASTFM_USERNAME, bot
from userbot.events import register

# =================== CONSTANT ===================
LFM_BIO_ENABLED = "```last.fm current music to bio is now enabled.```"
LFM_BIO_DISABLED = "```last.fm current music to bio is now disabled. Bio reverted to default.```"
LFM_BIO_RUNNING = "```last.fm current music to bio is already running.```"
ERROR_MSG = "```last.fm module halted, got an unexpected error.```"

ARTIST = 0
SONG = 0

BIOPREFIX = BIO_PREFIX

LASTFMCHECK = False
RUNNING = False
# ================================================


@register(outgoing=True, pattern="^.lastfm")
async def last_fm(lastFM):
    """ For .lastfm command, fetch scrobble data from last.fm. """
    if not lastFM.text[0].isalpha() and lastFM.text[0] not in ("/", "#", "@", "!"):
        await lastFM.edit("Processing...")
        preview = None
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        username = f"https://www.last.fm/user/{LASTFM_USERNAME}"
        if playing is not None:
            try:
                image = User(LASTFM_USERNAME, lastfm).get_now_playing().get_cover_image()
            except IndexError:
                image = None
                pass
            tags = gettags(isNowPlaying=True, playing=playing)
            rectrack = parse.quote_plus(f"{playing}")
            rectrack = sub("^", "https://www.youtube.com/results?search_query=", rectrack)
            if image:
                output = f"[‎]({image})[{LASTFM_USERNAME}]({username}) __is now listening to:__\n\n• [{playing}]({rectrack})\n`{tags}`"
                preview = True
            else:
                output = f"[{LASTFM_USERNAME}]({username}) __is now listening to:__\n\n• [{playing}]({rectrack})\n`{tags}`"
        else:
            recent = User(LASTFM_USERNAME, lastfm).get_recent_tracks(limit=3)
            playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
            output = f"[{LASTFM_USERNAME}]({username}) __was last listening to:__\n\n"
            for i, track in enumerate(recent):
                print(i) # vscode hates the i being there so lets make it chill
                printable = artist_and_song(track)
                tags = gettags(track)
                rectrack = parse.quote_plus(str(printable))
                rectrack = sub("^", "https://www.youtube.com/results?search_query=", rectrack)
                output += f"• [{printable}]({rectrack})\n"
                if tags:
                    output += f"`{tags}`\n\n"
        if preview is not None:
            await lastFM.edit(f"{output}", parse_mode='md', link_preview=True)
        else:
            await lastFM.edit(f"{output}", parse_mode='md')


def gettags(track=None, isNowPlaying=None, playing=None):
    if isNowPlaying:
        tags = playing.get_top_tags()
        arg = playing
        if not tags:
            tags = playing.artist.get_top_tags()
    else:
        tags = track.track.get_top_tags()
        arg = track.track
    if not tags:
        tags = arg.artist.get_top_tags()
    tags = "".join([" #" + t.item.__str__() for t in tags[:5]])
    tags = sub("^ ", "", tags)
    tags = sub(" ", "_", tags)
    tags = sub("_#", " #", tags)
    return tags


def artist_and_song(track):
    return f"{track.track}"


async def get_curr_track():
    global ARTIST
    global SONG
    global LASTFMCHECK
    global RUNNING
    oldartist = ""
    oldsong = ""
    while LASTFMCHECK:
        try:
            RUNNING = True
            playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
            song = playing.get_title()
            artist = playing.get_artist()
            oldsong = environ.get("oldsong", None)
            oldartist = environ.get("oldartist", None)
            if playing is not None and\
            song != oldsong and artist != oldartist:
                environ["oldsong"] = str(song)
                environ["oldartist"] = str(artist)
                lfmbio = f"{BIOPREFIX} 🎧: {artist} - {song}"
                try:
                    await bot(UpdateProfileRequest(about=lfmbio))
                except AboutTooLongError:
                    short_bio = f"🎧: {song}"
                    await bot(UpdateProfileRequest(about=short_bio))
        except AttributeError:
            await bot(UpdateProfileRequest(about=DEFAULT_BIO))
        LASTFMCHECK = False
        await sleep(2)
        await dirtyfix()
    RUNNING = False
                


async def dirtyfix():
    global LASTFMCHECK
    LASTFMCHECK = True
    await sleep(4)
    await get_curr_track()


@register(outgoing=True, pattern="^.enablelastfmbio$")
async def en_lastbio(enlfmbio):
    setrecursionlimit(700000)
    if not LASTFMCHECK:
        environ["errorcheck"] = "0"
        await enlfmbio.edit(LFM_BIO_ENABLED)
        await dirtyfix()
    else:
        await enlfmbio.edit(LFM_BIO_RUNNING)


@register(outgoing=True, pattern="^.disablelastfmbio$")
async def dis_lastbio(dislfmbio):
    global LASTFMCHECK
    global RUNNING
    LASTFMCHECK = False
    RUNNING = False
    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
    await dislfmbio.edit(LFM_BIO_DISABLED)


CMD_HELP.update({
    'lastfm': ".lastfm\
    \nUsage: Shows currently scrobbling track or most recent scrobbles if nothing is playing."
})
CMD_HELP.update({
    "enablelastfmbio": "Usage: Enable last.fm bio updating"
})
CMD_HELP.update({
    "disablelastfmbio": "Usage: Disable last.fm bio updating"
})

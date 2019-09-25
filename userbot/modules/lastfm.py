from asyncio import sleep
from os import environ
from re import sub
from sys import setrecursionlimit
from urllib import parse

from pylast import User, WSError
from telethon.errors import AboutTooLongError
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

from userbot import (BIO_PREFIX, BOTLOG, BOTLOG_CHATID, CMD_HELP, DEFAULT_BIO,
                     LASTFM_USERNAME, bot, is_redis_alive, lastfm)
from userbot.events import register
from userbot.modules.dbhelper import (getlastfmcheck, getuserID, lfgetartist,
                                      lfgetLogging, lfgetsong, lfsetartist,
                                      lfsetLogging, lfsetsong, setlastfmcheck,
                                      setuserID)

# =================== CONSTANT ===================
LFM_BIO_ENABLED = "```last.fm current music to bio is now enabled.```"
LFM_BIO_DISABLED = "```last.fm current music to bio is now disabled. Bio reverted to default.```"
LFM_BIO_RUNNING = "```last.fm current music to bio is already running.```"
LFM_BIO_ERR = "```No option specified.```"
LFM_LOG_ENABLED = "```last.fm logging to bot log is now enabled.```"
LFM_LOG_DISABLED = "```last.fm logging to bot log is now disabled.```"
LFM_LOG_ERR = "```No option specified.```"
ERROR_MSG = "```last.fm module halted, got an unexpected error.```"

if BIO_PREFIX:
    BIOPREFIX = BIO_PREFIX
else:
    BIOPREFIX = None
# ================================================


@register(outgoing=True, pattern="^.lastfm$")
async def last_fm(lastFM):
    """ For .lastfm command, fetch scrobble data from last.fm. """
    await lastFM.edit("Processing...")
    if not is_redis_alive():
        lastFM.edit("Who forgot their Redis?")
        return
    preview = None
    playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
    username = f"https://www.last.fm/user/{LASTFM_USERNAME}"
    if playing is not None:
        try:
            image = User(LASTFM_USERNAME,
                         lastfm).get_now_playing().get_cover_image()
        except IndexError:
            image = None

        tags = gettags(isNowPlaying=True, playing=playing)
        rectrack = parse.quote_plus(f"{playing}")
        rectrack = sub("^", "https://www.youtube.com/results?search_query=",
                       rectrack)
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
            print(i)  # vscode hates the i being there so lets make it chill
            printable = artist_and_song(track)
            tags = gettags(track)
            rectrack = parse.quote_plus(str(printable))
            rectrack = sub("^",
                           "https://www.youtube.com/results?search_query=",
                           rectrack)
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


async def get_curr_track(lfmbio):
    if not is_redis_alive():
        return
    oldartist = ""
    oldsong = ""
    while getlastfmcheck():
        try:
            if getuserID() == 0:
                setuserID(await lfmbio.client.get_me().id)
            user_info = await bot(GetFullUserRequest(await getuserID()))
            playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
            song = playing.get_title()
            await lfsetsong(song)
            artist = playing.get_artist()
            await lfsetartist(artist)
            oldsong = environ.get("oldsong", None)
            oldartist = environ.get("oldartist", None)
            if playing is not None and await lfgetsong() != oldsong and await lfgetartist() != oldartist:
                environ["oldsong"] = await lfgetsong()
                environ["oldartist"] = await lfgetartist()
                if BIOPREFIX:
                    lfmbio = f"{BIOPREFIX} 🎧: {await lfgetartist()} - {await lfgetsong()}"
                else:
                    lfmbio = f"🎧: {await lfgetartist()} - {await lfgetsong()}"
                try:
                    if BOTLOG and await lfgetLogging():
                        await bot.send_message(
                            BOTLOG_CHATID,
                            f"Attempted to change bio to\n{lfmbio}")
                    await bot(UpdateProfileRequest(about=lfmbio))
                except AboutTooLongError:
                    short_bio = f"🎧: {await lfgetsong()}"
                    await bot(UpdateProfileRequest(about=short_bio))
            else:
                if playing is None and user_info.about != DEFAULT_BIO:
                    await sleep(6)
                    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                    if BOTLOG and await lfgetLogging():
                        await bot.send_message(
                            BOTLOG_CHATID, f"Reset bio back to\n{DEFAULT_BIO}")
        except AttributeError:
            try:
                if user_info.about != DEFAULT_BIO:
                    await sleep(6)
                    await bot(UpdateProfileRequest(about=DEFAULT_BIO))
                    if BOTLOG and await lfgetLogging():
                        await bot.send_message(
                            BOTLOG_CHATID, f"Reset bio back to\n{DEFAULT_BIO}")
            except FloodWaitError as err:
                if BOTLOG and await lfgetLogging():
                    await bot.send_message(BOTLOG_CHATID,
                                           f"Error changing bio:\n{err}")
        except FloodWaitError as err:
            if BOTLOG and await lfgetLogging():
                await bot.send_message(BOTLOG_CHATID,
                                       f"Error changing bio:\n{err}")
        except WSError as err:
            if BOTLOG and await lfgetLogging():
                await bot.send_message(BOTLOG_CHATID,
                                       f"Error changing bio:\n{err}")
        await sleep(2)


@register(outgoing=True, pattern=r"^.lastbio (\S*)")
async def lastbio(lfmbio):
    if not is_redis_alive():
        return
    arg = lfmbio.pattern_match.group(1)
    if arg == "on":
        setrecursionlimit(700000)
        lastfmchknottrue = await getlastfmcheck() == "False"
        if lastfmchknottrue:
            await setlastfmcheck("True")
            environ["errorcheck"] = "0"
            await lfmbio.edit(LFM_BIO_ENABLED)
            await sleep(4)
            await get_curr_track(lfmbio)
        else:
            await lfmbio.edit(LFM_BIO_RUNNING)
    elif arg == "off":
        await setlastfmcheck("False")
        await bot(UpdateProfileRequest(about=DEFAULT_BIO))
        await lfmbio.edit(LFM_BIO_DISABLED)
    else:
        await lfmbio.edit(LFM_BIO_ERR)


@register(outgoing=True, pattern=r"^.lastlog (\S*)")
async def lastlog(lstlog):
    if not is_redis_alive():
        return
    arg = lstlog.pattern_match.group(1)
    await lfsetLogging("False")
    if arg == "on":
        await lfsetLogging("True")
        await lstlog.edit(LFM_LOG_ENABLED)
    elif arg == "off":
        await lfsetLogging("False")
        await lstlog.edit(LFM_LOG_DISABLED)
    else:
        await lstlog.edit(LFM_LOG_ERR)


CMD_HELP.update(
    {
        'lastfm': ".lastfm\n"
                  "Usage: Shows currently scrobbling track"
                  "or most recent scrobbles if nothing is playing."
    }
)

CMD_HELP.update(
    {
        'lastbio' : '.lastbio <on/off>\n'
                    'Usage: Enable or disable last.fm bio update'
    }
)

CMD_HELP.update(
    {
        'lastlog' : 'lastlog <on/off>\n'
                    'Usage: Enable or disable lastFM bio logging'
    }
)

# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various scrapers. """

import os
from re import findall, sub
from shutil import rmtree
from urllib.parse import quote_plus

import asyncurban
from emoji import get_emoji_regexp
from google_images_download import google_images_download
from googletrans import LANGUAGES, Translator
from gtts import gTTS, gTTSError
from requests import get
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, WOLFRAM_ID
from userbot.events import register, grp_exclude

# Default language to EN
LANG = "en"


@register(outgoing=True, pattern=r"^.img (.*)")
@grp_exclude()
async def img_sampler(event):
    """For .img command, search and return images matching the query."""
    await event.edit("Processing...")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 2
    response = google_images_download.googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst
    )
    rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


@register(outgoing=True, pattern=r"^.google(?: |$)(.*)")
@grp_exclude()
async def gsearch(q_event):
    """For .google command, do a Google search."""
    textx = await q_event.get_reply_message()
    query = q_event.pattern_match.group(1)

    if query:
        pass
    elif textx:
        query = textx.text
    else:
        await q_event.edit(
            "`Pass a query as an argument or reply " "to a message for Google search!`"
        )
        return

    await q_event.edit("`Searching...`")

    search_args = (str(query), 1)
    googsearch = GoogleSearch()
    try:
        gresults = await googsearch.async_search(*search_args)
        msg = ""
        for i in range(0, 5):
            try:
                title = gresults["titles"][i]
                link = gresults["links"][i]
                desc = gresults["descriptions"][i]
                msg += f"{i+1}. [{title}]({link})\n`{desc}`\n\n"
            except IndexError:
                break
        await q_event.edit(
            "**Search Query:**\n`" + query + "`\n\n**Results:**\n" + msg,
            link_preview=False,
        )
    except NoResultsOrTrafficError as error:
        if BOTLOG:
            await q_event.client.send_message(
                BOTLOG_CHATID, f"`GoogleSearch error: {error}`"
            )
        return
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + query + "` was executed successfully",
        )


@register(outgoing=True, pattern=r"^.wiki (.*)")
@grp_exclude()
async def wiki(wiki_q):
    """For .google command, fetch content from Wikipedia."""
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Page not found.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        with open("output.txt", "w+") as output_file:
            output_file.write(result)
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption="`Output too large, sending as file.`",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query {match} was executed successfully"
        )

def parse_ud_url(match):
    group = match.group(1)

    return f'[{group}](https://www.urbandictionary.com/define.php?term={quote_plus(group)})'

@register(outgoing=True, pattern=r"^.ud (.*)")
@grp_exclude()
async def urban_dict(ud_e):
    """For .ud command, fetch content from Urban Dictionary."""
    await ud_e.edit("`Processing...`")
    query = ud_e.pattern_match.group(1)
    urban = asyncurban.UrbanDictionary()

    try:
        words = await urban.search(query)
        await urban.close()
    except asyncurban.WordNotFoundError:
        await ud_e.edit(f"Sorry, couldn't find any results for `{query}`.")
        return

    result = ""
    for i, word in enumerate(words):
        definition = sub(r'\[([^\]]*)\]', parse_ud_url, word.definition)
        result += (f"{i+1}. [{word.word}]({word.permalink}): {definition}\n")
        if word.example:
            example = sub(r'\[([^\]]*)\]', parse_ud_url, word.example)
            result += f"`Example(s)`: {example}"
        result += "\n"

    await ud_e.edit(result)

    if BOTLOG:
        await ud_e.client.send_message(
            BOTLOG_CHATID, "ud query " + query + " executed successfully."
        )


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
@grp_exclude()
async def text_to_speech(query):
    """For .tts command, a wrapper for Google Text-to-Speech."""
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit("`Give a text or reply to a " "message for Text-to-Speech!`")
        return

    try:
        tts = gTTS(message, tld="com", lang=LANG)
        tts.save("k.mp3")
    except AssertionError:
        await query.edit(
            "The text is empty.\n"
            "Nothing left to speak after pre-precessing, "
            "tokenizing and cleaning."
        )
        return
    except ValueError:
        await query.edit("Language is not supported.")
        return
    except RuntimeError:
        await query.edit("Error loading the languages dictionary.")
        return
    except gTTSError:
        await query.edit(
            "Error in Google Text-to-Speech API request! "
            "Check Paperplane logs for details."
        )
        return

    with open("k.mp3", "r"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
        os.remove("k.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "TTS of " + message + " executed successfully!"
            )
        await query.delete()


@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
@grp_exclude()
async def translateme(trans):
    """For .trt command, translate the given text using Google Translate."""
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Give a text or reply " "to a message to translate!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=LANG)
    except ValueError:
        await trans.edit("Invalid destination language.")
        return

    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**Source ({source_lan.title()}):**`\n{message}`**\n\
\nTranslation ({transl_lan.title()}):**`\n{reply_text.text}`"

    await trans.client.send_message(trans.chat_id, reply_text)
    await trans.delete()
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID, f"Translate query {message} was executed successfully"
        )


@register(pattern=r"^.lang (.*)", outgoing=True)
@grp_exclude()
async def lang(value):
    """For .lang command, change the default langauge of userbot scrapers."""
    global LANG
    LANG = value.pattern_match.group(1)
    await value.edit("Default language changed to **" + LANG + "**")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, "Default language changed to **" + LANG + "**"
        )


def deEmojify(inputString):
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)


@register(outgoing=True, pattern=r"^.wolfram (.*)")
@grp_exclude()
async def wolfram(wvent):
    """Wolfram Alpha API"""
    if WOLFRAM_ID is None:
        await wvent.edit(
            "Please set your WOLFRAM_ID first !\n"
            "Get your API KEY from [here](https://"
            "products.wolframalpha.com/api/)",
            parse_mode="Markdown",
        )
        return
    i = wvent.pattern_match.group(1)
    appid = WOLFRAM_ID
    server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={i}"
    res = get(server)
    await wvent.edit(f"**{i}**\n\n" + res.text, parse_mode="Markdown")
    if BOTLOG:
        await wvent.client.send_message(
            BOTLOG_CHATID, f".wolfram {i} was executed successfully"
        )


CMD_HELP.update(
    {
        "scrapers": [
            "Scrapers",
            " - `.img <query> lim=<n>`: Do an Image Search on Google and send n results. Default is 2.\n"
            " - `.google <query>`: Search Google for query (argument or reply).\n"
            " - `.wiki <query>`: Search Wikipedia for query.\n"
            " - `.ud <query>`: Search on Urban Dictionary for query.\n"
            " - `.tts <query>`: Text-to-Speech the query (argument or reply) to the saved language.\n"
            " - `.trt <query>`: Translate the query (argument or reply) to the saved language.\n"
            " - `.lang <lang>`: Changes the default language of trt and TTS modules.\n"
            " - `.wolfram <query>: Get answers to questions using WolframAlpha Spoken Results API.",
        ]
    }
)

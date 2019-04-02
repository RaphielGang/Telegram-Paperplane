# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for updating the userbot. Userbots can update themselves :)"""

import subprocess

from userbot import HELPER
from userbot.events import register


@register(outgoing=True, pattern="^.updatebleeding$")
async def bleeding_upstream(bleed):
    """ For .updatebleeding command, update from the staging branch. """
    await bleed.edit("`Please wait while I upstream myself!`")
    subprocess.run(
        [
            "git",
            "remote",
            "rm",
            "origin",
        ], stdout=subprocess.PIPE,)

    subprocess.run(
        [
            "git",
            "remote",
            "add",
            "origin",
            "https://github.com/baalajimaestro/Telegram-UserBot"
        ], stdout=subprocess.PIPE,)

    subprocess.run(
        [
            "git",
            "fetch",
            "origin"
        ], stdout=subprocess.PIPE,)

    subprocess.run(
        [
            "git",
            "checkout",
            "staging"
        ], stdout=subprocess.PIPE,
    )

    subprocess.run(
        [
            "git",
            "reset",
            "--hard",
            "origin/staging"
        ], stdout=subprocess.PIPE,)
    await bleed.edit("`Shutting down for the upstream, Restart the bot kthx`")
    bleed.client.disconnect()


@register(outgoing=True, pattern="^.updatestable$")
async def stable_upstream(stable):
    """ For .updatestable command, update from the master branch. """
    await stable.edit("`Please wait while I upstream myself!`")
    subprocess.run(
        [
            "git",
            "remote",
            "rm",
            "origin",
        ], stdout=subprocess.PIPE,)

    subprocess.run(
        [
            "git",
            "remote",
            "add",
            "origin",
            "https://github.com/baalajimaestro/Telegram-UserBot"
        ], stdout=subprocess.PIPE,)

    subprocess.run(
        [
            "git",
            "fetch",
            "origin"
        ], stdout=subprocess.PIPE,)

    subprocess.run(
        [
            "git",
            "checkout",
            "staging"
        ], stdout=subprocess.PIPE,
    )

    subprocess.run(
        [
            "git",
            "reset",
            "--hard",
            "origin/master"
        ], stdout=subprocess.PIPE,)
    await stable.edit("`Shutting down for the upstream, Restart the bot kthx`")
    stable.client.disconnect()

HELPER.update({
    "updatestable": ".updatestable\
    \nUsage: Updates the bot to the latest master branch."
})
HELPER.update({
    "updatebleeding": ".updatebleeding\
    \nUpdates the bot to the latest staging branch."
})

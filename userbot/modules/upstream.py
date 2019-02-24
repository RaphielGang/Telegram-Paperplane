# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

import subprocess

from userbot.events import register


@register(outgoing=True, pattern="^.updatebleeding$")
async def bleeding_upstream(bleed):
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

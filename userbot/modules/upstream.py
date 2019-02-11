import subprocess

from telethon import events

from userbot import bot


@bot.on(events.NewMessage(outgoing=True, pattern="^.updatebleeding$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.updatebleding$"))
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
    bot.disconnect()

@bot.on(events.NewMessage(outgoing=True, pattern="^.updatestable$"))
@bot.on(events.MessageEdited(outgoing=True, pattern="^.updatestable$"))
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
    bot.disconnect()

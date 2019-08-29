# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""
This module updates the userbot based on Upstream revision
"""

from os import remove, execl
import sys
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP
from userbot.events import register, errors_handler


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def is_off_br(br):
    off_br = ['master', 'staging', 'redis']
    for k in off_br:
        if k == br:
            return 1
    return


@register(outgoing=True, pattern="^.update(?: |$)(.*)")
@errors_handler
async def upstream(ups):
    "For .update command, check if the bot is up to date, update if specified"
    if not ups.text[0].isalpha() and ups.text[0] not in ("/", "#", "@", "!"):
        await ups.edit("`Checking for updates, please wait....`")
        conf = ups.pattern_match.group(1)
        off_repo = 'https://github.com/RaphielGang/Telegram-UserBot.git'

        try:
            txt = "`Oops.. Updater cannot continue due to "
            txt += "some problems occured`\n\n**LOGTRACE:**\n"
            repo = Repo()
        except NoSuchPathError as error:
            await ups.edit(f'{txt}\n`directory {error} is not found`')
            return
        except InvalidGitRepositoryError as error:
            await ups.edit(f'{txt}\n`directory {error} does \
                           not seems to be a git repository`')
            return
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Early failure! {error}`')
            return

        ac_br = repo.active_branch.name
        if not await is_off_br(ac_br):
            await ups.edit(
                f'**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). '
                'in that case, Updater is unable to identify '
                'which branch is to be merged. '
                'please checkout to any official branch`')
            return

        try:
            repo.create_remote('upstream', off_repo)
        except BaseException:
            pass

        ups_rem = repo.remote('upstream')
        ups_rem.fetch(ac_br)
        changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

        if not changelog:
            await ups.edit(
                f'\n`Your BOT is`  **up-to-date**  `with`  **{ac_br}**\n')
            return

        if conf != "now":
            changelog_str = f'**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`'
            if len(changelog_str) > 4096:
                await ups.edit(
                    "`Changelog is too big, view the file to see it.`")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await ups.client.send_file(
                    ups.chat_id,
                    "output.txt",
                    reply_to=ups.id,
                )
                remove("output.txt")
            else:
                await ups.edit(changelog_str)
            await ups.respond('`do \".update now\" to update`')
            return

        await ups.edit('`New update found, updating...`')
        ups_rem.fetch(ac_br)
        ups_rem.git.reset('--hard', 'FETCH_HEAD')
        await ups.edit('`Successfully Updated!\n'
                       'Bot is restarting... Wait for a second!`')
        await ups.client.disconnect()
        # Spin a new instance of bot
        execl(sys.executable, sys.executable, *sys.argv)
        # Shut the existing one down
        exit()


CMD_HELP.update({
    'update':
    '.update\
\nUsage: Check if the main userbot repository has any\
updates and show changelog if so.\
\n\n.update now\
\nUsage: Update your userbot, if there are any\
updates in the main userbot repository.'
})

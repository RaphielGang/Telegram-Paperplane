# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""
This module updates the userbot based on Upstream revision
"""

import sys
from os import execl, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, HEROKU_APIKEY, HEROKU_APPNAME
from userbot.events import register
import os

async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def is_off_br(br):
    off_br = ['master', 'staging', 'redis']
    if br in off_br:
        return 1
    return


@register(outgoing=True, pattern="^.update(?: |$)(.*)")
async def upstream(ups):
    "For .update command, check if the bot is up to date, update if specified"
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
            await ups.edit(  "`Changelog is too big, view the file to see it.`")
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

    if HEROKU_APIKEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await ups.edit(
                '`[HEROKU] Please set up the HEROKU_APPNAME variable to be able to update userbot.`'
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f'{txt}\n`Invalid Heroku credentials for updating userbot dyno.`'
            )
            repo.__del__()
            return
        await ups.edit('`[HEROKU]\
                        \nUserbot dyno build in progress, please wait for it to complete.`'
                       )
        os.popen(f'cd /app && git pull origin master')
        os.popen(f'git config --global user.email "example@example.com" && git config --global user.name "Example"')
        os.popen('cd /app && git add -f userbot.session config.env && git commit -m "Update userbot"')
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_APIKEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Here is the error log:\n{error}`')
            repo.__del__()
            return
        await ups.edit('`Successfully Updated!\n'
                       'Restarting, please wait...`')
    else:
        # Classic Updater, for using on PC
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        reqs_upgrade = await update_requirements()
        await ups.edit('`Successfully Updated!\n'
                       'Bot is restarting... Wait for a second!`')
        # Spin a new instance of bot
        args = [sys.executable, "-m", "userbot"]
        execle(sys.executable, *args, environ)
        return


CMD_HELP.update({
    'update':
    '.update\n'
    'Usage: Check if the main userbot repository has any'
    'updates and show changelog if so.'
})

CMD_HELP.update({
    'update':
    '.update now\n'
    'Usage: Update your userbot, if there are any'
    'updates in the main userbot repository.'
})

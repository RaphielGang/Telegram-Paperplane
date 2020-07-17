# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""
This module updates the userbot based on Upstream revision
"""

import sys
from os import execl, remove, path
import heroku3

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, HEROKU_APIKEY, HEROKU_APPNAME, STRING_SESSION
from userbot.events import register, grp_exclude


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def is_off_br(br):
    off_br = ['master', 'staging']
    if br in off_br:
        return 1
    return


@register(outgoing=True, pattern="^.update(?: |$)(.*)")
@grp_exclude()
async def upstream(ups):
    "For .update command, check if the bot is up to date, update if specified"
    await ups.edit("`Checking for updates, please wait....`")
    conf = ups.pattern_match.group(1)
    off_repo = 'https://github.com/RaphielGang/Telegram-Paperplane.git'

    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems.`\n\n**LOGTRACE:**\n"
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
            'In that case, Updater is unable to perform a successful update. '
            'Please checkout to any official branch.`')
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog:
        await ups.edit(f'\n`Your BOT is `**up-to-date**` with `**{ac_br}**\n')
        return

    if conf != "now":
        changelog_str = f'**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ups.edit("`Changelog is too big, view the file to see it.`")
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
        await ups.respond('`Use the \".update now\" command to update`')
        return

    await ups.edit('`New update found, updating...`')

    ups_rem.fetch(ac_br)
    repo.git.reset('--hard', 'FETCH_HEAD')

    if HEROKU_APIKEY != None:
        # Heroku configuration, which can rebuild the Docker image with newer changes
        heroku = heroku3.from_key(HEROKU_APIKEY)
        if HEROKU_APPNAME != None:
            try:
                heroku_app = heroku.apps()[HEROKU_APPNAME]
            except KeyError:
                await ups.edit(
                    "```Error: HEROKU_APPNAME config is invalid! Make sure an app with that "
                    "name exists and your HEROKU_APIKEY config is correct.```")
                return
        else:
            await ups.edit(
                "```Error: HEROKU_APPNAME config is not set! Make sure to set your "
                "Heroku Application name in the config.```")
            return

        await ups.edit(
            "`Heroku configuration found! Updater will try to update and restart Paperplane"
            "automatically if succeeded. Try checking if Paperplane is alive by using the"
            "\".alive\" command after a few minutes.`")
        if not STRING_SESSION:
            repo.git.add('userbot.session', force=True)
        if path.isfile('config.env'):
            repo.git.add('config.env', force=True)

        # Set git config for commiting session and config
        repo.config_writer().set_value("user", "name",
                                       "Paperplane Updater").release()
        repo.config_writer().set_value("user", "email",
                                       "<>").release()  # No Email

        # Make a new commit with session and commit (if they exist), this is only temporary to move them to the Docker image
        # Allow empty commit if there is nothing to commit (string session + env vars)
        repo.git.commit("--allow-empty", "-m 'Commit userbot.session and config.env'")

        heroku_remote_url = heroku_app.git_url.replace(
            "https://", f"https://api:{HEROKU_APIKEY}@")

        remote = None
        if 'heroku' in repo.remotes:
            remote = repo.remote('heroku')
            remote.set_url(heroku_remote_url)
        else:
            remote = repo.create_remote('heroku', heroku_remote_url)

        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as e:
            await ups.edit(f'{txt}\n`Early failure! {e}`')
            return
    else:
        # Heroku configs not set, just restart the bot
        await ups.edit(
            '`Successfully Updated!\n'
            'Paperplane is restarting... Wait for a few seconds, then '
            'check if Paperplane is alive by using the ".alive" command.`')

        await ups.client.disconnect()
        # Spin a new instance of bot
        execl(sys.executable, sys.executable, *sys.argv)
        # Shut the existing one down
        exit()


CMD_HELP.update({
    "updater": [
        'Updater',
        " - `.update`: Check if the main repository has any updates and show changelog if so.\n"
        " - `.update now`: Update Paperplane if there are any updates available."
    ]
})

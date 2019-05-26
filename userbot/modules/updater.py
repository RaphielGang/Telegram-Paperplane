# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from userbot import HELPER
from userbot.events import register
from git import Repo, exc


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


@register(outgoing=True, pattern="^.update ?(.*)")
async def upstream(ups):
    await ups.edit("`Checking for updates, please wait....`")
    conf = ups.pattern_match.group(1)
    off_repo = 'https://github.com/baalajimaestro/Telegram-UserBot.git'

    try:
        txt = "`Oops.. Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except exc.NoSuchPathError as e:
        await ups.edit(f'{txt}    `directory {e} is not found`')
        return
    except exc.InvalidGitRepositoryError as e:
        await ups.edit(f'{txt}    `directory {e} does not seems to be a git repository`')
        return

    if (repo.is_dirty() or len(repo.untracked_files)):
        await ups.edit('**[UPDATER]:** `Looks like you have some un-committed files and changes. you have to commit them first, then updater can continue`')
        return

    ac_br = repo.active_branch.name
    if not await is_off_br(ac_br):
        await ups.edit(f'**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). in that case, Updater is unable to identify which branch is to be merged. please checkout to any official branch`')
        return

    try:
        repo.create_remote('upstream', off_repo)
    except:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog:
        await ups.edit(f'\n`Your BOT is`  **up-to-date**  `with`  **{ac_br}**\n')
        return

    if conf != "now":
        await ups.edit(f'**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`')
        await ups.respond('`do \".update now\" to update`')
        return

    await ups.edit('`New update found, updating...`')

    try:
        ups_rem.pull(ac_br)
    except exc.GitCommandError:
        await ups.edit('`Update failed.. due to merge conflicts \nreverting all temp changes`')
        repo.git.reset('--hard')
        return

    await ups.edit('`Successfully Updated!!\nBot is switching off now.. restart kthx`')
    await ups.client.disconnect()


HELPER.update({
    'update': '.update\
\nUsage: Checks if the main userbot repository has any updates and shows changelog if so.\
\n\n.update now\
\nUsage: Updates your userbot if there are any updates in the main userbot repository.'
})

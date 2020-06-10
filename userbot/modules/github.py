import re
from typing import List

from github import UnknownObjectException
from github.NamedUser import NamedUser
from github.Repository import Repository

from userbot import CMD_HELP, github
from userbot.events import register
from userbot.utils import parse_arguments
from userbot.utils.tgdoc import *

GITHUB_REPO_RE = r"(?:github\.com\/|^|\s+)([\w\d_\-]+)\/([\w\d_\-.]+)"


@register(outgoing=True, pattern=r"^\.gh(\s+[\S\s]+|$)")
async def github_info(e):
    if not github:
        await e.edit("Github information has not been set up")
        return

    message = e.pattern_match.group(1)
    reply_message = await e.get_reply_message()

    if message:
        message = message.strip()
        args, message = parse_arguments(message, [
            'general', 'owner', 'all'
        ])
    else:
        args = {}

    if not message:
        if reply_message:
            message = reply_message.message.strip()
        else:
            await e.edit(str(Bold("Can't fetch repo information with no repo")))
            return

    repos = re.findall(GITHUB_REPO_RE, message)
    if repos:
        await e.edit(f"Fetching information for {len(repos)} repo(s)...")
        valid_repos: List[str] = []
        invalid_repos: List[str] = []
        for user, repo in repos:
            try:
                r: Repository = github.get_repo(f"{user}/{repo}")
                repo = await build_repo_message(r, args)
                valid_repos.append(str(repo))
            except UnknownObjectException:
                invalid_repos.append(f"{user}/{repo}")
                pass

        message = ""
        if valid_repos:
            message += '\n\n'.join(valid_repos)
        if invalid_repos:
            message += '\n'.join(invalid_repos)

        await e.edit(message)
    else:
        await e.edit("No GitHub repos found")
        return


async def build_repo_message(repo, args):
    show_general = args.get('general', True)
    show_owner = args.get('owner', False)
    show_all = args.get('all', False)

    if show_all:
        show_general = True
        show_owner = True

    title = Link(repo.name, repo.html_url)

    if show_general:
        general = SubSection(Bold("general"),
                             KeyValueItem("id", Code(repo.id)),
                             KeyValueItem("full name", Code(repo.full_name)),
                             KeyValueItem("stars", Code(repo.stargazers_count)),
                             KeyValueItem("watchers", Code(repo.watchers_count)),
                             KeyValueItem("forks", Code(repo.forks_count)),
                             KeyValueItem("language", Code(repo.language)),
                             KeyValueItem("is fork", Code(repo.fork)),
                             KeyValueItem("issues", Code(repo.open_issues)))
    else:
        general = None

    if show_owner:
        owner: NamedUser = github.get_user(repo.owner.login)
        bio = str(owner.bio)[:50] + (str(owner.bio)[50:] and '..')

        owner_info = SubSection(Bold("owner"),
                                KeyValueItem("id", owner.id),
                                KeyValueItem("login", owner.login),
                                KeyValueItem("name", owner.name),
                                KeyValueItem("bio", bio),
                                KeyValueItem("company", owner.company),
                                KeyValueItem("email", owner.email),
                                KeyValueItem("followers", owner.followers),
                                KeyValueItem("following", owner.following),
                                KeyValueItem("repos", owner.public_repos))
    else:
        owner_info = None

    return Section(
        title,
        general if show_general else None,
        owner_info if show_owner else None
    )


CMD_HELP.update({"github": ["GitHub",
                           " - `gh (repo)`: Displays information related to a github repo. Similar to `.user`.\n\n"
                           "Repos can be in the format `https://github.com/user/repo` or just `user/repo`.\n\n"
                           "**Options:\n\n**"
                           "`.general`: Display general information related to the repo.\n"
                           "`.owner`: Display information about the repo owner.\n"
                           "`.all`: Display everything.\n\n"
                           "**All commands can be used with** `.`"]
                 })

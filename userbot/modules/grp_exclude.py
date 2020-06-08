# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Paperplane Exclude, a module for excluding a group from the Paperplane event handler. """

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive)
from userbot.modules.dbhelper import (get_excludes, get_exclude,
                                      add_exclude_group, remove_exclude_group,
                                      is_excluded)
from userbot.events import register, grp_exclude


@register(outgoing=True, pattern="^.exclude ?(-?[0-9]+)? ?(in|all)?")
async def exclude_grp(excl):
    if not is_mongo_alive():
        await excl.edit("`Database connections failing!`")
        return

    chat_id = excl.pattern_match.group(1)
    exclude_type = excl.pattern_match.group(2)

    if not chat_id:
        chat_id = excl.chat_id

    ###### Exclude types:
    ### 0: Blocks incoming events only [default] (also force_exclude events)
    ### 1: Blocks every event (both incoming and outgoing)
    if not exclude_type or exclude_type.lower() == 'in':
        exclude_type_num = 0
        exclude_type = 'in'
    if exclude_type == 'all':
        exclude_type_num = 1

    await add_exclude_group(chat_id, exclude_type_num)

    await excl.edit(
        f"`This chat (ID: {chat_id}, Exclude type: {exclude_type}) has been added to Paperplane Exclude!`"
    )
    return


@register(outgoing=True, pattern="^.unexclude ?(-?[0-9]+)?")
async def unexclude_grp(excl):
    if not is_mongo_alive():
        await excl.edit("`Database connections failing!`")
        return

    chat_id = excl.pattern_match.group(1)

    if not chat_id:
        chat_id = excl.chat_id

    await remove_exclude_group(chat_id)

    await excl.edit(
        f"`This chat (ID: {chat_id}) has been removed from Paperplane Exclude!`"
    )
    return


@register(outgoing=True, pattern="^.listexclude")
@grp_exclude()
async def listexclude_grp(excl):
    if not is_mongo_alive():
        await excl.edit("`Database connections failing!`")
        return

    excl_list = await get_excludes()

    resp = ""
    for item in excl_list:
        if item['excl_type'] == 0:
            excl_type = 'in'
        else:
            excl_type = 'all'

        resp += f"- Chat ID: `{item['chatid']}`, Exclude type: `{excl_type}`\n"

    if resp != "":
        resp = f"`Here is the list of chats in Paperplane Exclude:`\n\n{resp}"
    else:
        resp = f"`There are no chats in Paperplane Exclude.`"

    await excl.edit(resp)
    return


CMD_HELP.update({
    "paperplane exclude": [
        'Paperplane Exclude',
        "PAPERPLANE EXCLUDE IS CURRENTLY BETA, and some features MAY NOT WORK PROPERLY. "
        "We are not responsible for any bugs found in the module.\n"
        " - `.exclude [chatid] (in|all)`: Exclude this (or the specified) group from the Paperplane event handler. "
        "This means that Paperplane will behave restricted in that group, by not responding to incoming "
        "triggers (such as AFK, filters, notes...) and/or your commands (such as .alive).\n"
        " - `.unexclude [chatid]`: Unexclude this (or the specified) group from the Paperplane event handler. Paperplane "
        "will behave like normally on that group after this.\n"
        " - `.listexclude`: Lists every excluded chat, (Chat ID and exclude type). \n\n"
        "Exclude types:\n"
        " - `in`: This will exclude all incoming message, and will only allow outgoing messages. "
        "It means that you will be able to execute commands yourself, but other people won't be "
        "able to trigger Papepplane with notes, filters and mentioning while AFK. Also, AFK module "
        "won't un-AFK you when you send a message.\n"
        " - `all`: This will exclude *all* events, meaning that everything excluded by `in` plus "
        "you won't be able to execute commands. Paperplane will pretend not to exist when this option "
        "is set.\n"
        "`P.S.: The .exclude and .unexclude commands will still work even if that chat is excluded.`"
    ]
})

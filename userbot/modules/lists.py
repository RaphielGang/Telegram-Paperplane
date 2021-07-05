# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping lists. """

import re

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive, is_redis_alive
from userbot.events import register, grp_exclude
from userbot.modules.dbhelper import (
    add_list,
    delete_list,
    get_list,
    get_lists,
    set_list,
)

# =================== CONSTANTS ===================

DB_FAILED = "`Database connections failed!`"
NO_LISTS = "`There are no saved lists in this chat or globally.`"
CHK_HELP = "`Check `**.help lists**` for more info about Lists.`"
LIST_NOT_FOUND = "`List {} not found!`"
LIST_HEADER = "[Paperplane-List] List **{}({})**\n\n"

# =================================================


@register(outgoing=True, pattern="^.lists$")
@grp_exclude()
async def lists_active(event):
    """For .lists command, list all of the lists saved in a chat."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    message = NO_LISTS
    lists = await get_lists(event.chat_id)
    if lists.count() != 0:
        message = "Lists saved in this chat:\n"

        for _list in lists:
            message += "🔹 **{} ({})**\n".format(
                _list["name"], "Local" if (_list["chat_id"] != 0) else "Global"
            )

    await event.edit(message)


@register(outgoing=True, pattern=r"^.dellist ?(\w*)")
@grp_exclude()
async def removelists(event):
    """For .dellist command, delete list with the given name."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    textx = await event.get_reply_message()
    listname = None

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list to delete!` {CHK_HELP}")
        return

    _list = await get_list(event.chat_id, listname)

    if await delete_list(event.chat_id, listname) is False:
        await event.edit("`Couldn't find list:` **{}**".format(listname))
        return

    await event.edit("`Deleted list:` **{}**".format(listname))

    if BOTLOG:
        listat = "global storage" if _list["chat_id"] == 0 else str(event.chat_id)
        await event.client.send_message(
            BOTLOG_CHATID, f"Removed list {listname} from {listat}"
        )


@register(outgoing=True, pattern=r"^.new(g)?list (\w*)")
@grp_exclude()
async def addlist(event):
    """For .new(g)list command, saves lists in a chat."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    is_global = event.pattern_match.group(1) == "g"

    listname = event.pattern_match.group(2)
    content = event.text.partition(f"{listname} ")[2].splitlines()

    msg = "`List {} successfully. Use` ${} `to get it.`"

    chatid = 0 if is_global else event.chat_id

    if await add_list(chatid, listname, content) is False:
        await event.edit(msg.format("updated", listname))
    else:
        await event.edit(msg.format("created", listname))

    if BOTLOG:
        listat = "global storage" if is_global else str(event.chat_id)
        await event.client.send_message(
            BOTLOG_CHATID, f"Created list {listname} in {listat}"
        )


@register(outgoing=True, pattern=r"^.addlistitems? ?(\w*)\n((.|\n*)*)")
@grp_exclude()
async def add_list_items(event):
    """For .addlistitems command, add item(s) to a list."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    textx = await event.get_reply_message()
    listname = None

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)

    if not listname:
        return_msg = f"`Pass a list to add items into it!` {CHK_HELP}"
        await event.edit(return_msg)
        return

    _list = await get_list(event.chat_id, listname)

    if not _list:
        await x.edit(LIST_NOT_FOUND.format(listname))

    content = _list["items"]
    newitems = event.pattern_match.group(2)
    content.extend(newitems.splitlines())

    msg = "`Item(s) added successfully to the list.\n\n"
    msg += "New item(s):\n"
    msg += f"{newitems}\n\n"
    msg += f"Use` ${listname} `to get the list.`"

    if await add_list(event.chat_id, listname, content) is False:
        await event.edit(msg)
    else:
        await event.edit(LIST_NOT_FOUND.format(listname))
        return

    if BOTLOG:
        listat = "global storage" if _list["chat_id"] else str(event.chat_id)

        log = f"Added item(s) to {listname} in {listat}.\n"
        log += "New items:\n"
        log += f"{newitems}"

        await event.client.send_message(BOTLOG_CHATID, log)


@register(outgoing=True, pattern=r"^.editlistitem ?(\w*)? ([0-9]+) (.*)")
@grp_exclude()
async def edit_list_item(event):
    """For .editlistitem command, edit an individual item on a list."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    textx = await event.get_reply_message()
    listname = None
    arg_indexes = event.pattern_match.group(2)

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
        arg_indexes = event.pattern_match.group(1) + " " + arg_indexes
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list!` {CHK_HELP}")
        return

    item_number = int(event.pattern_match.group(2))

    _list = await get_list(event.chat_id, listname)
    content = _list["items"]
    content[item_number - 1] = event.pattern_match.group(3)

    msg = f"`Item {item_number} edited successfully.\n"
    msg += f"Use` ${listname} `to get the list.`"

    if await add_list(event.chat_id, listname, content) is False:
        await event.edit(msg)
    else:
        await event.edit(LIST_NOT_FOUND.format(listname))

    if BOTLOG:
        listat = "global storage" if _list["chat_id"] else str(event.chat_id)

        log = f"Edited item {item_number} of "
        log += f"{listname} in {listat} successfully."
        await event.client.send_message(BOTLOG_CHATID, log)


@register(outgoing=True, pattern=r"^.rmlistitems? ?(\w*)? ([0-9 ]+)")
@grp_exclude()
async def rmlistitems(event):
    """For .rmlistitem command, remove an item from the list."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    await event.edit("`Removing...`")

    textx = await event.get_reply_message()
    listname = None
    arg_indexes = event.pattern_match.group(2)

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
        arg_indexes = event.pattern_match.group(1) + " " + arg_indexes
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list to remove items from!` {CHK_HELP}")
        return

    # Check if the argument contains only numbers and whitespaces
    if re.match("^ *[0-9][0-9 ]*$", arg_indexes):
        unwanted_indexes = list(map(int, arg_indexes.split()))
    else:
        await event.edit(f"`Error: Wrong arguments! {CHK_HELP}`")
        return

    _list = await get_list(event.chat_id, listname)

    try:
        for elem in sorted(unwanted_indexes, reverse=True):
            del _list["items"][elem - 1]
    except TypeError:
        await event.edit(LIST_NOT_FOUND.format("listname"))
        return
    except IndexError:
        await event.edit(
            f"`Item `**{unwanted_indexes}**\
` in list `**{listname}**` not found!`"
        )
        return

    msg = "`Item(s) {} removed from the list successfully. \
Use` ${} `to get the list.`"

    if await add_list(event.chat_id, listname, _list["items"]) is False:
        await event.edit(msg.format(unwanted_indexes, listname))
    else:
        await event.edit(f"List {listname} doesn't exist!")

    if BOTLOG:
        listat = "global storage" if _list["chat_id"] else str(event.chat_id)
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Removed item(s) {str(unwanted_indexes)} from {listname} in {listat}",
        )


@register(outgoing=True, pattern=r"^.setlist ?(\w*)? (global|local)")
@grp_exclude()
async def setliststate(event):
    """For .setlist command, changes the state of a list."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    _futureState = event.pattern_match.group(2)
    changeToGlobal = None

    if _futureState == "global":
        changeToGlobal = True
    elif _futureState == "local":
        changeToGlobal = False

    textx = await event.get_reply_message()
    listname = None

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list to remove!` {CHK_HELP}")
        return

    _list = await get_list(event.chat_id, listname)

    chatid = 0 if changeToGlobal else event.chat_id

    msg = f"`The state of list {listname} changed to \
{_futureState} successfully.`"

    if await set_list(_list["chat_id"], listname, chatid) is True:
        await event.edit(msg)
    else:
        await event.edit(f"`List {listname} not found!`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"Changed state of list {listname} to {_futureState}"
        )


@register(
    pattern=r"\$\w*", disable_edited=True, ignore_unsafe=True, disable_errors=True
)
@grp_exclude()
async def lists_logic(event):
    """Lists logic."""
    try:
        if not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return

            listname = event.text[1:]
            _list = await get_list(event.chat_id, listname)
            if _list:
                storage = "None"
                if _list["chat_id"] == 0:
                    storage = "global"
                else:
                    storage = str(_list["chat_id"])

                return_str = LIST_HEADER.format(listname, storage)

                if _list["items"]:
                    for i, item in enumerate(_list["items"]):
                        return_str += f"{i+1}. {item}\n"

                    return_str += f"\n{CHK_HELP}"
                else:
                    return_str = f"`This list is empty!` {CHK_HELP}"

                await event.reply(return_str)
    except BaseException:
        pass


@register(pattern=r"^.getlist ?(\w*)?")
@grp_exclude()
async def getlist_logic(event):
    """For .getlist, get the list by the name."""
    if not (await event.get_sender()).bot:
        if not is_mongo_alive() or not is_redis_alive():
            return

        textx = await event.get_reply_message()
        listname = None

        if textx:
            x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
            listname = x.group(1)
        elif event.pattern_match.group(1):
            listname = event.pattern_match.group(1)
        else:
            await event.edit(f"`Pass a list to get!` {CHK_HELP}")
            return

        _list = await get_list(event.chat_id, listname)
        if _list:
            storage = "None"
            if _list["chat_id"] == 0:
                storage = "global"
            else:
                storage = str(_list["chat_id"])

            return_str = LIST_HEADER.format(listname, storage)

            if _list["items"]:
                for i, item in enumerate(_list["items"]):
                    return_str += f"{i+1}. {item}\n"
            else:
                return_str = "`This list is empty!`"

            await event.edit(return_str)
        else:
            await event.edit(f"`List {listname} not found!`")


CMD_HELP.update(
    {
        "lists": [
            "Lists",
            " - `.lists`: Get all of the lists (both local and global).\n"
            " - `$listname`: Get the list called 'listname'.\n"
            " - `.getlist <listname>`: Same as $listname.\n"
            " - `.newlist <listname> <items>`: Creates a local list called 'listname' and adds items to it. "
            "Separate items with a newline. Local lists are only accessible from a specific chat.\n"
            " - `.newglist <listname> <items>`: Creates a global list called 'listname' and adds items to it. "
            "Separate items with a newline. Global lists are accessible from every chat you are in.\n"
            " - `.dellist <listname>`: Deletes the list called 'listname'.\n"
            " - `.addlistitem(s) <listname> <items>`: Add new items to the list called 'listname'. "
            "Separate items with a newline. The first items should start from a newline.\n"
            " - `.rmlistitem(s) <listname> <indexes>`: Remove items accompanying the indexes from the list called 'listname'. "
            "Indexes are the numbers which the item is on the list. You can remove multiple items at once from the list.\n"
            " - `.editlistitem <listname> <item_number> <new_content>`: Edit item item_number in listname, changing the "
            "content to new_content.\n"
            " - `.setlist <listname> <local|global>`: Change the status of a list to local (accessible only from the current chat) "
            "or global (accessible from every chat you are in.).\n\n"
            "By replying to a Paperplane List message(identified by "
            "\n'[Paperplane-List]' in the beginning of a userbot message), "
            "\nyou can omit <listname> from all commands (except $<listname>)."
            "\nPaperplane will recognize the list from the replied message.",
        ]
    }
)

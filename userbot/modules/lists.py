# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module containing commands for keeping lists. """

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP,
                     is_mongo_alive, is_redis_alive)
from userbot.modules.dbhelper import (get_list, get_lists,
                                      add_list, delete_list,
                                      set_list)
from userbot.events import register


@register(outgoing=True, pattern="^.lists$")
async def lists_active(event):
    """ For .lists command, list all of the lists saved in a chat. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

        message = "`There are no saved lists in this chat`"
        lists = await get_lists(event.chat_id)
        if lists.count() != 0:
            message = "Lists saved in this chat:\n"

            for _list in lists:
                message += "🔹 **{} ({})**\n".format(
                    _list["name"],
                    "Local" if (_list["chat_id"] != 0) else "Global"
                )

        await event.edit(message)


@register(outgoing=True, pattern=r"^.rmlist (\w*)")
async def removelists(event):
    """ For .rmlist command, delete list with the given name."""
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return
        listname = event.pattern_match.group(1)
        _list = await get_list(event.chat_id, listname)

        if await delete_list(event.chat_id, listname) is False:
            await event.edit("`Couldn't find list:` **{}**"
                             .format(listname))
        else:
            await event.edit("`Successfully deleted list:` **{}**"
                             .format(listname))

        if BOTLOG:
            listat = "global storage" if _list['chat_id'] == 0 else str(
                event.chat_id)
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Removed list {listname} from {listat}"
            )


@register(outgoing=True, pattern=r"^.add(g)?list (\w*)")
async def addlist(event):
    """ For .add(g)list command, saves lists in a chat. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

        is_global = event.pattern_match.group(1) == "g"

        listname = event.pattern_match.group(2)
        content = event.text.partition(f"{listname} ")[2].splitlines()

        msg = "`List {} successfully. Use` ${} `to get it`"

        chatid = 0 if is_global else event.chat_id

        if await add_list(chatid, listname, content) is False:
            await event.edit(msg.format('updated', listname))
        else:
            await event.edit(msg.format('added', listname))

        if BOTLOG:
            listat = "global storage" if is_global else str(event.chat_id)
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Added list {listname} to {listat}"
            )


@register(outgoing=True, pattern=r"^.addlistitem(s)? (\w*)")
async def add_list_items(event):
    """ For .addlistitems command, add item(s) to a list. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

        listname = event.pattern_match.group(2)
        _list = await get_list(event.chat_id, listname)
        content = _list['items']

        content.extend(event.text.partition(f"{listname} ")[2].splitlines())

        msg = "`Items added successfully to the list. \
Use` ${} `to get the list.`"

        if await add_list(event.chat_id, listname, content) is False:
            await event.edit(msg.format(listname))
        else:
            await event.edit(f"List {listname} doesn't exist!")

        if BOTLOG:
            listat = "global storage" if _list['chat_id'] else str(
                event.chat_id)
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Added items {content} to {listname} in {listat}"
            )


@register(outgoing=True, pattern=r"^.editlistitem (\w*) ([0-9]+)")
async def edit_list_item(event):
    """ For .editlistitem command, edit an individual item on a list. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

        listname = event.pattern_match.group(1)
        item_number = int(event.pattern_match.group(2))

        _list = await get_list(event.chat_id, listname)
        content = _list['items']
        content[item_number - 1] = event.text.partition(
            f"{listname} {item_number} "
        )[2]

        msg = f"`Item {item_number} edited successfully. \
Use` ${listname} `to get the list.`"

        if await add_list(event.chat_id, listname, content) is False:
            await event.edit(msg)
        else:
            await event.edit(f"List {listname} doesn't exist!")

        if BOTLOG:
            listat = "global storage" if _list['chat_id'] else str(
                event.chat_id)
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Edited item {item_number} of {listname} in {listat} successfully."
            )


@register(outgoing=True, pattern=r"^.rmlistitem (\w*) ([0-9]+)")
async def rmlistitems(event):
    """ For .rmlistitem command, remove an item from the list. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

        listname = event.pattern_match.group(1)
        item_number = int(event.pattern_match.group(2))

        _list = await get_list(event.chat_id, listname)

        content = _list['items']
        del content[item_number - 1]

        msg = "`Item {} removed from the list successfully. \
Use` ${} `to get the list.`"

        if await add_list(event.chat_id, listname, content) is False:
            await event.edit(msg.format(item_number, listname))
        else:
            await event.edit(f"List {listname} doesn't exist!")

        if BOTLOG:
            listat = "global storage" if _list['chat_id'] else str(
                event.chat_id)
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Removed item {str(item_number)} from {listname} in {listat}"
            )


@register(outgoing=True, pattern=r"^.setlist (\w*) (\w*)")
async def setliststate(event):
    """ For .setlist command, changes the state of a list. """
    cmd = event.text[0]
    if not cmd.isalpha() and cmd not in ("/", "#", "@", "!"):
        if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

        _futureState = event.pattern_match.group(2)
        changeToGlobal = None

        if _futureState == "global":
            changeToGlobal = True
        elif _futureState == "local":
            changeToGlobal = False

        listname = event.pattern_match.group(1)
        _list = await get_list(event.chat_id, listname)

        chatid = 0 if changeToGlobal else event.chat_id

        msg = f"`The state of list {listname} changed to \
{_futureState} successfully.`"

        if await set_list(_list['chat_id'], listname, chatid) is True:
            await event.edit(msg)
        else:
            await event.edit(f"`List {listname} not found!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"Changed state of list {listname} to {_futureState}"
            )


@register(pattern=r"\$\w*", disable_edited=True)
async def lists_logic(event):
    """ Lists logic. """
    try:
        if not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return

            listname = event.text[1:]
            _list = await get_list(event.chat_id, listname)
            if _list:
                return_str = ""

                if _list['items']:
                    for i, item in enumerate(_list['items']):
                        return_str += f"{i+1}. {item}\n"
                else:
                    return_str = "`This list is empty!`"

                await event.reply(return_str)
    except BaseException:
        pass

CMD_HELP.update({
    "lists": "\
.lists\
\nUsage: Get all of the lists (both local and global)\
\n\n$<listname>\
\nUsage: Gets the list with name listname\
\n\n.addlist <listname> <items>\
\nUsage: Saves items as a list with the name listname. \
Separate items with a new line.\
\n\n.addglist <listname> <items>\
\nUsage: Saves items as a global list with the name listname. \
Separate items with a new line. Accessible from every chat.\
\n\n.rmlist <listname>\
\nUsage: Delete the list with name listname.\
\n\n.addlistitem(s) <listname> <items>\
\nUsage: Add items to the list listname. \
Separate items with a new line.\
\n\n.rmlistitem <listname> <item_number>\
\nUsage: Delete the item with the number item_number in the \
list with the name listname.\
\n\n.editlistitem <listname> <item_number> <new_content>\
\nUsage: Edit item item_number in listname, changing the \
content to new_content\
\n\n.setlist <listname> <local|global>\
\nUsage: Change the status of a list to local \
(accessible only from the current chat), or global \
(accessible from every chat).\
"
})

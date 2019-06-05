from userbot import MONGO


async def mute(chatid, userid):
    if await is_muted(chatid, userid) is True:
        return False
    else:
        MONGO.mutes.insert_one({
            'chat_id': chatid,
            'user_id': userid
        })
        return True


async def is_muted(chatid, userid):
    is_muted = MONGO.mutes.find_one({
        'chat_id': chatid,
        'user_id': userid
    })

    if not is_muted:
        return False
    else:
        return True


async def unmute(chatid, userid):
    if await is_muted(chatid, userid) is False:
        return False
    else:
        MONGO.mutes.delete_one({
            'chat_id': chatid,
            'user_id': userid
        })
        return True


async def get_muted(chatid):
        muted_db = MONGO.mutes.find({
            'chat_id': int(chatid)
        })

        muted = []
        for user in muted_db:
            muted.append(user["user_id"])

        return muted


async def gmute(userid):
    if await is_gmuted(userid) is True:
        return False
    else:
        MONGO.gmutes.insert_one({
            'user_id': userid
        })
        return True


async def is_gmuted(userid):
    is_gmuted = MONGO.gmutes.find_one({
        'user_id': userid
    })

    if not is_gmuted:
        return False
    else:
        return True


async def ungmute(userid):
    if await is_gmuted(userid) is False:
        return False
    else:
        MONGO.gmutes.delete_one({
            'user_id': userid
        })
        return True


async def get_gmuted():
    gmuted_db = MONGO.gmutes.find()
    gmuted = []

    for user in gmuted_db:
        gmuted.append(user["user_id"])

    return gmuted


async def get_filter(chatid, keyword):
    return MONGO.filters.find_one({
        'chat_id': chatid,
        'keyword': keyword
    })


async def get_filters(chatid):
    return MONGO.filters.find({
        'chat_id': chatid
    })


async def add_filter(chatid, keyword, msg):
    to_check = await get_filter(chatid, keyword)

    if not to_check:
        MONGO.filters.insert_one({
            'chat_id': chatid,
            'keyword': keyword,
            'msg': msg
        })
    else:
        MONGO.filters.update_one({
            '_id': to_check["_id"],
            'chat_id': to_check["chat_id"],
            'keyword': to_check["keyword"],
            "$set": {
                'msg': msg
            }
        })


async def delete_filter(chatid, keyword):
    to_check = await get_filter(chatid, keyword)

    if not to_check:
        return False
    else:
        MONGO.filters.delete_one({
            '_id': to_check["_id"],
            'chat_id': to_check["chat_id"],
            'keyword': to_check["keyword"],
            'msg': to_check["msg"]
        })

        return True

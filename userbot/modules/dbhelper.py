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

from userbot import MONGO, REDIS
import pymongo


# Mutes
async def mute(chatid, userid):
    if await is_muted(chatid, userid) is True:
        return False
    else:
        MONGO.mutes.insert_one({'chat_id': chatid, 'user_id': userid})
        return True


async def is_muted(chatid, userid):
    is_muted = MONGO.mutes.find_one({'chat_id': chatid, 'user_id': userid})

    if not is_muted:
        return False
    else:
        return True


async def unmute(chatid, userid):
    if await is_muted(chatid, userid) is False:
        return False
    else:
        MONGO.mutes.delete_one({'chat_id': chatid, 'user_id': userid})
        return True


async def get_muted(chatid):
    muted_db = MONGO.mutes.find({'chat_id': int(chatid)})

    muted = []
    for user in muted_db:
        muted.append(user["user_id"])

    return muted


# GMutes
async def gmute(userid):
    if await is_gmuted(userid) is True:
        return False
    else:
        MONGO.gmutes.insert_one({'user_id': userid})
        return True


async def is_gmuted(userid):
    is_gmuted = MONGO.gmutes.find_one({'user_id': userid})

    if not is_gmuted:
        return False
    else:
        return True


async def ungmute(userid):
    if await is_gmuted(userid) is False:
        return False
    else:
        MONGO.gmutes.delete_one({'user_id': userid})
        return True


async def get_gmuted():
    gmuted_db = MONGO.gmutes.find()
    gmuted = []

    for user in gmuted_db:
        gmuted.append(user["user_id"])

    return gmuted


# Filters
async def get_filters(chatid):
    return MONGO.filters.find({'chat_id': chatid})


async def get_filter(chatid, keyword):
    return MONGO.filters.find_one({'chat_id': chatid, 'keyword': keyword})


async def add_filter(chatid, keyword, msg):
    to_check = await get_filter(chatid, keyword)

    if not to_check:
        MONGO.filters.insert_one({
            'chat_id': chatid,
            'keyword': keyword,
            'msg': msg
        })
        return True
    else:
        MONGO.filters.update_one(
            {
                '_id': to_check["_id"],
                'chat_id': to_check["chat_id"],
                'keyword': to_check["keyword"],
            }, {"$set": {
                'msg': msg
            }})

        return False


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


# Notes
async def get_notes(chatid):
    return MONGO.notes.find({'chat_id': chatid})


async def get_note(chatid, name):
    return MONGO.notes.find_one({'chat_id': chatid, 'name': name})


async def add_note(chatid, name, text):
    to_check = await get_note(chatid, name)

    if not to_check:
        MONGO.notes.insert_one({'chat_id': chatid, 'name': name, 'text': text})

        return True
    else:
        MONGO.notes.update_one(
            {
                '_id': to_check["_id"],
                'chat_id': to_check["chat_id"],
                'name': to_check["name"],
            }, {"$set": {
                'text': text
            }})

        return False


async def delete_note(chatid, name):
    to_check = await get_note(chatid, name)

    if not to_check:
        return False
    else:
        MONGO.notes.delete_one({
            '_id': to_check["_id"],
            'chat_id': to_check["chat_id"],
            'name': to_check["name"],
            'text': to_check["text"],
        })


# Lists
async def get_lists(chatid):
    return MONGO.lists.find({'$or': [{'chat_id': chatid}, {'chat_id': 0}]})


async def get_list(chatid, name):
    return MONGO.lists.find_one({
        '$or': [{
            'chat_id': chatid
        }, {
            'chat_id': 0
        }],
        'name': name
    })


async def add_list(chatid, name, items):
    to_check = await get_list(chatid, name)

    if not to_check:
        MONGO.lists.insert_one({
            'chat_id': chatid,
            'name': name,
            'items': items
        })

        return True
    else:
        MONGO.lists.update_one(
            {
                '_id': to_check["_id"],
                'chat_id': to_check["chat_id"],
                'name': to_check["name"],
            }, {"$set": {
                'items': items
            }})

        return False


async def delete_list(chatid, name):
    to_check = await get_list(chatid, name)

    if not to_check:
        return False
    else:
        MONGO.lists.delete_one({
            '_id': to_check["_id"],
            'chat_id': to_check["chat_id"],
            'name': to_check["name"],
            'items': to_check["items"],
        })


async def set_list(oldchatid, name, newchatid):
    to_check = await get_list(oldchatid, name)

    if not to_check:
        return False
    else:
        MONGO.lists.update_one(
            {
                '_id': to_check["_id"],
                'name': to_check["name"],
                'items': to_check["items"]
            }, {"$set": {
                'chat_id': newchatid
            }})

        return True


##########


async def approval(userid):
    to_check = MONGO.pmpermit.find_one({'user_id': userid, 'approval': True or False})

    if to_check is None:
        MONGO.pmpermit.insert_one({'user_id': userid, 'approval': False})

        return False
    elif to_check['approval'] is False:
        return False
    elif to_check['approval'] is True:
        return True

    
async def approve(userid):
    if await approval(userid) is True:
        return False
    else:
        MONGO.pmpermit.update_one({'user_id': userid},
                                  {"$set": {
                                      'approval': True
                                  }})
        return True   
    

async def disapprove(userid):
    if await approval(userid) is False:
        return False
    else:
        MONGO.pmpermit.update_one({'user_id': userid},
                                  {"$set": {
                                      'approval': False
                                  }})
        return True

async def autoapproval(autouserid):
    to_check = MONGO.pmpermit.find_one({'auto_user_id': autouserid})

    if to_check is None:
        MONGO.pmpermit.insert_one({'auto_user_id': autouserid, 'autoapproval': False})

        return False
    elif to_check['autoapproval'] is False:
        return False
    elif to_check['autoapproval'] is True:
        return True
    

async def autoapprove(autouserid):
    if await autoapproval(autouserid) is True:
        MONGO.pmpermit.update_one({'auto_user_id': autouserid},
                                  {"$set": {
                                      'autoapproval': False
                                  }})
        return
    else:
        MONGO.pmpermit.update_one({'auto_user_id': autouserid},
                                  {"$set": {
                                      'autoapproval': True
                                  }})
        return 


async def block_pm(userid):
    if await approval(userid) is False:
        return False
    else:
        await disapprove(userid)

        return True


async def notif_state():
    state = dict()
    state_db = MONGO.notif.find()

    for stat in state_db:
        state.update(stat)

    if not state:
        MONGO.notif.insert_one({'state': True})
        return True
    elif state["state"] is False:
        return False
    elif state["state"] is True:
        return True


async def __notif_id():
    id_real = dict()
    id_db = MONGO.notif.find()

    for id_s in id_db:
        id_real.update(id_s)

    return id_real["_id"]


async def notif_on():
    if await notif_state() is True:
        return False
    else:
        MONGO.notif.update({'_id': await __notif_id()},
                           {"$set": {
                               'state': True
                           }})
        return True


async def notif_off():
    if await notif_state() is False:
        return False
    else:
        MONGO.notif.update({'_id': await __notif_id()},
                           {"$set": {
                               'state': False
                           }})
        return True


def strb(redis_string):
    return str(redis_string)[2:-1]


async def is_afk():
    to_check = REDIS.get('is_afk')
    if to_check:
        return True
    else:
        return False


async def afk(reason):
    REDIS.set('is_afk', reason)


async def afk_reason():
    return strb(REDIS.get('is_afk'))


async def no_afk():
    REDIS.delete('is_afk')


# Fbans


async def get_fban():
    return MONGO.fban.find()


async def add_chat_fban(chatid):
    if await is_fban(chatid) is True:
        return False
    else:
        MONGO.fban.insert_one({'chatid': chatid})


async def remove_chat_fban(chatid):
    if await is_fban(chatid) is False:
        return False
    else:
        MONGO.fban.delete_one({'chatid': chatid})
        return True


async def is_fban(chatid):
    if not MONGO.fban.find_one({"chatid": chatid}):
        print("FAILED on fed")
        return False
    else:
        return True


# Gbans


async def get_gban():
    return MONGO.gban.find()


async def add_chat_gban(chatid):
    if await is_gban(chatid) is True:
        print("FAILED")
        return False
    else:
        MONGO.gban.insert_one({'chatid': chatid})


async def remove_chat_gban(chatid):
    if await is_gban(chatid) is False:
        return False
    else:
        MONGO.gban.delete_one({'chatid': chatid})
        return True


async def is_gban(chatid):
    if not MONGO.gban.find_one({"chatid": chatid}):
        return False
    else:
        return True


# Time
async def get_time():
    return MONGO.misc.find_one({'timec': {
        '$exists': True
    }}, {
        'timec': 1,
        'timezone': 1
    })


async def set_time(country, timezone=1):
    to_check = await get_time()

    if to_check:
        MONGO.misc.update_one(
            {
                '_id': to_check['_id'],
                'timec': to_check['timec'],
                'timezone': to_check['timezone']
            }, {"$set": {
                'timec': country,
                'timezone': timezone
            }})
    else:
        MONGO.misc.insert_one({'timec': country, 'timezone': timezone})


# Weather
async def get_weather():
    return MONGO.misc.find_one({'weather_city': {
        '$exists': True
    }}, {'weather_city': 1})


async def set_weather(city):
    to_check = await get_weather()

    if to_check:
        MONGO.misc.update_one(
            {
                '_id': to_check['_id'],
                'weather_city': to_check['weather_city']
            }, {"$set": {
                'weather_city': city
            }})
    else:
        MONGO.misc.insert_one({'weather_city': city})


# Paperplane Exclude
async def get_excludes():
    return MONGO.excludes.find()


async def get_exclude(chatid):
    return MONGO.excludes.find_one({'chatid': chatid})


async def add_exclude_group(chatid, excl_type=1):
    is_excl = await get_exclude(chatid)

    if is_excl:
        MONGO.excludes.update_one(
            {
                '_id': is_excl['_id'],
                'chatid': is_excl['chatid'],
                'excl_type': is_excl['excl_type']
            }, {"$set": {
                'chatid': chatid,
                'excl_type': excl_type
            }})
    else:
        MONGO.excludes.insert_one({'chatid': chatid, 'excl_type': excl_type})


async def remove_exclude_group(chatid):
    if await is_excluded(chatid) is False:
        return False
    else:
        MONGO.excludes.delete_one({'chatid': chatid})
        return True


async def is_excluded(chatid):
    if not await get_exclude(chatid):
        return False
    else:
        return True
    
# PICTURES
async def alive_pic(apic):
    to_check = MONGO.pictures.find_one({'apic': apic, 'alive_pic': True or False})
    
    if to_check is None:
        MONGO.pictures.insert_one({'id': 'ALIVE_PIC', 'apic': apic, 'alive_pic': True})
        return False
    elif to_check['alive_pic'] is False:
        return False
    elif to_check['alive_pic'] is True:
        return True
    
    
async def set_alive_pic(apic):
    if MONGO.pictures.find_one({'id': 'ALIVE_PIC', 'apic': apic}) is None:
        MONGO.pictures.insert_one({'id': 'ALIVE_PIC', 'apic': apic})
    else:
        MONGO.pictures.replace_one({'id': 'ALIVE_PIC', 'apic': apic})
        
        
async def get_alive_pic():
    pic = MONGO.pictures.find_one({'id': 'ALIVE_PIC'})['apic']
    return pic

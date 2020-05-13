# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Module that holding database components """

from userbot import MONGO, REDIS


# Mutes
async def mute(chatid, userid):
    """ Add muted person ID to database """
    if await is_muted(chatid, userid) is True:
        return False

    MONGO.mutes.insert_one({'chat_id': chatid, 'user_id': userid})
    return True


async def is_muted(chatid, userid):
    """ Return if the current ID is muted """
    muted = MONGO.mutes.find_one({'chat_id': chatid, 'user_id': userid})
    if not muted:
        return False

    return True


async def unmute(chatid, userid):
    """ Remove a ID for unmute event"""
    if await is_muted(chatid, userid) is False:
        return False

    MONGO.mutes.delete_one({'chat_id': chatid, 'user_id': userid})
    return True


async def get_muted(chatid):
    """ Grab if the current userID is muted """
    muted_db = MONGO.mutes.find({'chat_id': int(chatid)})

    muted = []
    for user in muted_db:
        muted.append(user["user_id"])

    return muted


# GMutes
async def gmute(userid):
    """ Add a globally muted person ID into database """
    if await is_gmuted(userid) is True:
        return False

    MONGO.gmutes.insert_one({'user_id': userid})
    return True


async def is_gmuted(userid):
    """ Return if the current ID is globally muted """
    gmuted = MONGO.gmutes.find_one({'user_id': userid})
    if not gmuted:
        return False

    return True


async def ungmute(userid):
    """ Remove a ID for ungmute event """
    if await is_gmuted(userid) is False:
        return False

    MONGO.gmutes.delete_one({'user_id': userid})
    return True


async def get_gmuted():
    """ Grab if the current ID is globally muted """
    gmuted_db = MONGO.gmutes.find()
    gmuted = []

    for user in gmuted_db:
        gmuted.append(user["user_id"])

    return gmuted


# Filters
async def get_filters(chatid):
    """ Find filters for specified ChatID """
    return MONGO.filters.find({'chat_id': chatid})


async def get_filter(chatid, keyword):
    """ Get filter content for the specified keyword """
    return MONGO.filters.find_one({'chat_id': chatid, 'keyword': keyword})


async def add_filter(chatid, keyword, msg):
    """ Add a filter into Database """
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
            },
            {
                "$set": {'msg': msg}
            })

        return False


async def delete_filter(chatid, keyword):
    """ Delete a filter from Database """
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
    """ Find notes from specific ChatID """
    return MONGO.notes.find({'chat_id': chatid})


async def get_note(chatid, name):
    """ Get notes from specific ChatID """
    return MONGO.notes.find_one({'chat_id': chatid, 'name': name})


async def add_note(chatid, name, text):
    """ Add a note into the Database """
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
            },
            {
                "$set": {'text': text}
            })

        return False


async def delete_note(chatid, name):
    """ Delete a note from Database """
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
    """ Find list for specified ChatID """
    return MONGO.lists.find({'$or': [{'chat_id': chatid}, {'chat_id': 0}]})


async def get_list(chatid, name):
    """ Get list for specified ChatID """
    return MONGO.lists.find_one({
        '$or': [{
            'chat_id': chatid
        }, {
            'chat_id': 0
        }],
        'name': name
    })


async def add_list(chatid, name, items):
    """ Add a list into the Database """
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
    """ Delete a list from the Database """
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
    """ Set a list """
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
    """ Add approved ID into Database """
    to_check = MONGO.pmpermit.find_one({'user_id': userid})

    if to_check is None:
        MONGO.pmpermit.insert_one({'user_id': userid, 'approval': False})

        return False
    elif to_check['approval'] is False:
        return False
    elif to_check['approval'] is True:
        return True


async def approve(userid):
    """ Find if a ID is approved """
    if await approval(userid) is True:
        return False

    MONGO.pmpermit.update_one({
        'user_id': userid
    }, {
        "$set": {'approval': True}
    })
    return True


async def block_pm(userid):
    """ Add a blocked person ID into database """
    if await approval(userid) is False:
        return False

    MONGO.pmpermit.update_one({
        'user_id': userid
    }, {
        "$set": {'approval': False}
    })
    return True


async def notif_state():
    """ Get notification setting """
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
    """ Get notification ID from Database """
    id_real = dict()
    id_db = MONGO.notif.find()

    for id_s in id_db:
        id_real.update(id_s)

    return id_real["_id"]


async def notif_on():
    """ Return if notification is enabled """
    if await notif_state() is True:
        return False

    MONGO.notif.update(
        {
            '_id': await __notif_id()
        },
        {
            "$set": {'state': True}
        }
    )
    return True


async def notif_off():
    """ Return if notification is disabled """
    if await notif_state() is False:
        return False

    MONGO.notif.update(
        {
            '_id': await __notif_id()
        },
        {
            "$set": {'state': False}
        }
    )
    return True


async def is_afk():
    """ Return if the user is AFK """
    to_check = REDIS.get('is_afk')
    if to_check:
        return True

    return False


async def afk(reason):
    """ Set AFK Reason """
    REDIS.set('is_afk', reason)


async def afk_reason():
    """ Get AFK Reason """
    return REDIS.get('is_afk').decode("UTF-8")


async def no_afk():
    """ Remove AFK Reason and state """
    REDIS.delete('is_afk')

# Spotify


async def sfsetartist(artist):
    """ Set Spotify Artist """
    REDIS.set('sfartist', artist)


async def sfsetsong(song):
    """ Set Spotify Song """
    REDIS.set('sfsong', song)


async def spotifycheck(spotifychck):
    """ Set Spotify Check (Status) """
    REDIS.set('spotifycheck', spotifychck)


async def exceptionexist(olexception):
    """ Set if Spotify had exception before """
    REDIS.set('exceptionexist', olexception)


async def sfgetsong():
    """ Get Spotify Song """
    return REDIS.get('sfsong').decode("UTF-8")


async def sfgetartist():
    """ Get Spotify Artist """
    return REDIS.get('sfartist').decode("UTF-8")


async def getexception():
    """ Get if Spotify had exception before """
    exceptcheck = REDIS.get('exceptionexist')
    if exceptcheck is True:
        return True

    return False


async def getspotifycheck():
    """ Get Spotify Check (Status) """
    spotifychk = REDIS.get('spotifycheck')
    if spotifychk is True:
        return True

    return False

# LastFM


async def lfsetartist(artist):
    """ Set LastFM Artist """
    REDIS.set('lfartist', artist)


async def lfsetsong(song):
    """ Set LastFM Song """
    REDIS.set('lfsong', song)


async def setlastfmcheck(lastfmcheck):
    """ Set LastFM Check (Status) """
    REDIS.set('lastfmcheck', lastfmcheck)


async def setuserID(userid):
    """ Set UserID for LastFM """
    REDIS.set('userid', userid)


async def lfsetLogging(log):
    """ Set Logging for LastFM """
    REDIS.set('lflog', log)


async def lfgetartist():
    """ Get LastFM Artist """
    return REDIS.get('lfartist').decode("UTF-8")


async def lfgetsong():
    """ Get LastFM Song """
    return REDIS.get('lfsong').decode("UTF-8")


async def getlastfmcheck():
    """ Get LastFM Check (Status) """
    lastcheck = REDIS.get('lastfmcheck')
    if lastcheck is True:
        return True

    return False


async def getuserID():
    """ Get UserID for LastFM """
    return REDIS.get('userid')


async def lfgetLogging():
    """ Get Logging for LastFM """
    loggingup = REDIS.get('lflog')
    if loggingup is True:
        return True

    return False


# Fbans
async def get_fban():
    """ Find if a ID is fedbanned """
    return MONGO.fban.find()


async def add_chat_fban(chatid):
    """ Add a chat to execute fban into database """
    if await is_fban(chatid) is True:
        return False

    MONGO.fban.insert_one({'chatid': chatid})


async def remove_chat_fban(chatid):
    """ Remove chat that used for executing fban from database """
    if await is_fban(chatid) is False:
        return False

    MONGO.fban.delete_one({'chatid': chatid})
    return True


async def is_fban(chatid):
    """ Check if the current chat is on database """
    if not MONGO.fban.find_one({"chatid": chatid}):
        return False

    return True


# Gbans
async def get_gban():
    """ Find if a ID is gbanned """
    return MONGO.gban.find()


async def add_chat_gban(chatid):
    """ Add a chat to execute gban into database """
    if await is_gban(chatid) is True:
        return False

    MONGO.gban.insert_one({'chatid': chatid})


async def remove_chat_gban(chatid):
    """ Remove chat that used for executing gban from database """
    if await is_gban(chatid) is False:
        return False

    MONGO.gban.delete_one({'chatid': chatid})
    return True


async def is_gban(chatid):
    """ Check if the current chat is on database """
    if not MONGO.gban.find_one({"chatid": chatid}):
        return False

    return True


# Time
async def get_time():
    """ Get time variables from database """
    return MONGO.misc.find_one({'timec': {
        '$exists': True
    }}, {
        'timec': 1,
        'timezone': 1
    })


async def set_time(country, timezone=1):
    """ Set Time into database """
    to_check = await get_time()

    if to_check:
        MONGO.misc.update_one(
            {
                '_id': to_check['_id'],
                'timec': to_check['timec'],
                'timezone': to_check['timezone']
            },
            {
                "$set": {'timec': country,
                         'timezone': timezone
                         }
            }
        )
    else:
        MONGO.misc.insert_one({'timec': country, 'timezone': timezone})


# Weather
async def get_weather():
    """ Get weather variables from database """
    return MONGO.misc.find_one(
        {
            'weather_city': {'$exists': True}
        },
        {
            'weather_city': 1
        }
    )


async def set_weather(city):
    """ Set weather variables from database """
    to_check = await get_weather()

    if to_check:
        MONGO.misc.update_one(
            {
                '_id': to_check['_id'],
                'weather_city': to_check['weather_city']
            },
            {
                "$set": {'weather_city': city}
            }
        )
    else:
        MONGO.misc.insert_one({'weather_city': city})

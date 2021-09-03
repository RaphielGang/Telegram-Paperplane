"""MaplePlane Database - MongoDB and Redis"""

from userbot import maple_config

from pymongo import MongoClient
from redis import StrictRedis

# MongoDB setup.
MONGOCLIENT = MongoClient(maple_config.DATABASE_URL, 27017, serverSelectionTimeoutMS=1)
MONGO = MONGOCLIENT.userbot

def is_mongo_alive():
    try:
        MONGOCLIENT.server_info()
    except BaseException as error:
        print(error)
        return False
    return True

# Redis small setup.
# Redis will just be used for caching.
REDIS = StrictRedis(host='localhost', port=6379, db=0)

def is_redis_alive():
    try:
        REDIS.ping()
    except BaseException:
        return False
    return True

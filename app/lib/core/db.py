#encoding:utf-8

import pymongo
from config import Config
from log import logger

try:
    client = pymongo.MongoClient(host=Config.MONGODB_HOST, \
                                port=Config.MONGODB_PORT)
    mongo = client[Config.MONGODB_DB]
except Exception as ex:
    logger.exception(ex.message)
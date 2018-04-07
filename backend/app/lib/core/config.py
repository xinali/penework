#encoding:utf-8 

from datetime import date


class MongoDBConfig(object):
    MONGODB_HOST = '172.17.0.5' 
    MONGODB_PORT = 27017
    MONGODB_DB = 'penework'
    # masscan collection
    MONGODB_C_MSCAN = 'MScan'
    # nasscan collection
    MONGODB_C_NSCAN = 'NScan'
    MONGODB_C_PROJECTS = 'Projects'
    # USER = 'admin'
    # PASSWORD = 'testadmin'

class MScanConfig(MongoDBConfig):
    MSCAN_RATE = 30000
    MSCAN_SCAN_PORTS = '1-65535'
    MSCAN_TARGET_FILE = 'data/masscan/target.txt'
    MSCAN_RESULT_FILE = 'data/masscan/result/' + str(date.today()) + '.txt'
    # True: store data to mongodb 
    MSCAN_STORE_DATA = True
    # masscan object, for server just 1
    MSCAN_RUNNING = 1
    

class NScanConfig(MScanConfig):
    NSCAN_TIMEOUT = 5


class AppConfig(NScanConfig):
    DEBUG = True
    SECRET_KEY = '$fDqE3fvZTEeqCIDtM1P9Oe'
    TOKEN_KEY = 'motherfu4ck'
    EXPIRE_TIME = 86400 # 24 hours


class CeleryConfig(AppConfig):
    BROKER_URL = 'redis://127.0.0.1:6379/1'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
    CELERY_TASK_SERIALIZER = 'msgpack'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']


class Config(CeleryConfig):
    LOG_FILE = 'penework.log'
    SALT = '$2b$12$044d7t3tbLSz6v5uj49en.'
#encoding:utf-8 

from ..core.config import Config
from pymongo import MongoClient

def initdb():
    client = MongoClient(host=Config.MONGODB_HOST, port=Config.MONGODB_PORT)
    client.penework.users.drop()
    client.penework.roles.drop()

def register_log():
    pass
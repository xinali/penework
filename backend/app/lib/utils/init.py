#encoding:utf-8 

from ..core.config import Config
from pymongo import MongoClient
import time
import datetime


def generate_data(client):
    client.penework.Projects.drop()
    
    projects = {
        'pid': 1,
        'project_name': u'盛大渗透',
        'domain': 'sdo.com',
        'status': 'running',
        'create_time': datetime.datetime.now(),
        'description': u'盛大渗透测试项目'
    }
    client.penework.Projects.insert(projects)
    time.sleep(5)
    projects = {
        'pid': 2,
        'project_name': u'百度渗透',
        'domain': 'baidu.com',
        'status': 'done',
        'create_time': datetime.datetime.now(),
        'description': u'百度渗透测试项目'
    }
    client.penework.Projects.insert(projects)


def initdb():
    client = MongoClient(host=Config.MONGODB_HOST, port=Config.MONGODB_PORT)
    client.penework.users.drop()
    client.penework.roles.drop()

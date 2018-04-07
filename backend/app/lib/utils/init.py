#encoding:utf-8 

from ..core.config import Config
from pymongo import MongoClient
import time
import datetime


def generate_project(client):
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


def generate_ports(client):
    port_info = {
        'pid': 1, 
        'ip': '192.168.2.3',
        'port': 80,
        'banner': '<html><head></head><body>project pid is 1 shanda</body></html>',
        'time': datetime.datetime.now(),
        'title': u'盛大游戏官网',
        'hostname': 'this is test'
    }
    client.penework[Config.MONGODB_C_NSCAN].insert(port_info)
    time.sleep(5)

    port_info = {
        'pid': 1, 
        'ip': '192.165.99.89',
        'port': 60000,
        'banner': '<html><head></head><body>project pid is 1 shanda</body></html>',
        'time': datetime.datetime.now(),
        'title': u'盛大游戏官网',
        'hostname': 'this is test'
    }
    client.penework[Config.MONGODB_C_NSCAN].insert(port_info)

    port_info = {
        'pid': 1, 
        'ip': '192.168.2.3',
        'port': 80,
        'banner': '<html><head></head><body>project pid is 1 shanda</body></html>',
        'time': datetime.datetime.now(),
        'title': u'盛大游戏官网',
        'hostname': 'this is test'
    }
    client.penework[Config.MONGODB_C_NSCAN].insert(port_info)
    time.sleep(5)

    port_info = {
        'pid': 2, 
        'ip': '99.16.9.89',
        'port': 50000,
        'banner': '<html><head></head><body>project pid is 1 shanda</body></html>',
        'time': datetime.datetime.now(),
        'title': u'百度游戏官网',
        'hostname': 'this is test'
    }
    client.penework[Config.MONGODB_C_NSCAN].insert(port_info)

    port_info = {
        'pid': 2, 
        'ip': '88.1.9.77',
        'port': 50000,
        'banner': '<html><head></head><body>project pid is 1 shanda</body></html>',
        'time': datetime.datetime.now(),
        'title': u'百度游戏官网',
        'hostname': 'test'
    }
    client.penework[Config.MONGODB_C_NSCAN].insert(port_info)



def initdb():
    client = MongoClient(host=Config.MONGODB_HOST, port=Config.MONGODB_PORT)
    client.penework.users.drop()
    client.penework.roles.drop()
    generate_project(client)
    generate_ports(client)

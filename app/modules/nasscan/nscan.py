#encoding:utf-8

import sys
import os 
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../../")

import datetime
from utils import *
import lib.core.log import logger
from lib.core.db import mongo
from lib.core.config import Config


def run():
    scan_list = get_scanlists() 

    for data in scan_list:
        ip, port = data.split(':')
        banner = ''
        port = int(port)

        # scan port
        banner = scan_port(ip, port)  
        if not banner:
            continue

        # get hostname
        hostname = ip2hostname(ip)
        
        title, webinfo = try_web(ip, port)  
        time_ = datetime.datetime.now()
        if web_info:
            mongo[Config.MONGODB_C_NSCAN].insert({'ip': ip, 'port': port, 'banner': web_info, 'time': time_}})
        else:
            mongo[Config.MONGODB_C_NSCAN].insert({'ip': ip, 'port': port, 'banner': banner, 'title':title, time': time_}})
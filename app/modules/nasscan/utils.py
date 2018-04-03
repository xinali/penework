#encoding:utf-8


import sys
import os 
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../../")

import socket
import re
import requests
import lib.core.log import logger
from lib.core.db import mongo
from lib.core.config import Config

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def get_scan_lists(pid):
    timeout = Config.NSCAN_TIMEOUT
    open_ip_ports = {}
    try:
        masscan_result = mongo[Config.MONGODB_C_MSCAN].find({'pid':pid}, {'data':1, '_id':0})
        for data in masscan_result:
            open_ip_ports = data['data']

        # shuffle scan ip:port for bypassing firewall
        scan_list = []
        for ip, ports in open_ip_ports.items():
            for port in ports:
            scan_list.append(ip+':'+port)
        random.shuffle(scan_list)
        return scan_list
    except Exception as ex:
        logger.exception(ex.message)
    
def scan_port( ip, port):
    banner = ''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port))
    except Exception as e:
        logger.exception(e.message)
        return
    try:
        banner = sock.recv(1024)
        sock.close()
        if len(banner) <= 2:
            banner = 'NULL'
    except Exception, e:
        banner = 'NULL'

    logger.info('portscan: {ip} {port} is open'.format(ip=ip, port=port))
    try:
        if banner:
            banner = unicode(banner, errors='replace')
    except Exception as ex:
        logger.exception(ex.message)
        banner = 'NULL'
    return banner


def try_web(ip, port):
    session = requests.Session()
    session.verify = False
    # set retry count
    session.max_redirects = 3
    # set redirect false
    session.resolve_redirects = False
    timeout = Config.NSCAN_TIMEOUT

    banner = u''

    try:
        if port == 443:
            response = session.get("https://%s:%s" % (ip, port), timeout=timeout)
        else:
            response = session.get("http://%s:%s" % (ip, port), timeout=timeout)
        html = response.text
    except Exception as ex:
        logger.exception(ex.message)
    
    for key, value in response.headers:
        banner += key + ':' + value + '\r\n'
    banner += '\r\n' + html
    
    try:
        title = re.search(r'<title>(.*?)</title>', html, flags=re.I | re.M)
        if title: 
            title = title.group(1)
        else:
            title = 'NULL'
    except Exception as ex: 
        logger.exception(ex.message)
    
    return title, banner


def ip2hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        pass
    try:
        query_data = "\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20\x43\x4b\x41\x41" + \
                        "\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41" + \
                        "\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x00\x00\x21\x00\x01"
        dport = 137
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.settimeout(3)
        _s.sendto(query_data, (ip, dport))
        x = _s.recvfrom(1024)
        tmp = x[0][57:]
        hostname = tmp.split("\x00", 2)[0].strip()
        hostname = hostname.split()[0]
        return hostname
    except:
        pass
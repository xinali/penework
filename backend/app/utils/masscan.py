#encoding:utf-8 

import sys
import os 
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../../")

from datetime import date
from lib.core.log import logger
from lib.core.config import Config

class MScan(object):

    def __init__(self, pid=-1, scan_ip_range='127.0.0.1', scan_ports='1-65535', rate=10000):

        self.scan_ip_range = scan_ip_range
        self.scan_ports = scan_ports
        self.scan_rate = rate
        self.result_file = Config.MSCAN_RESULT_FILE
        self.store = Config.MSCAN_STORE_DATA
        self.pid = pid


    def analysis(self):
        result_fp = open(self.result_file, 'r')
        result_json = result_fp.readlines()
        result_fp.close()
        del result_json[0]
        del result_json[-1]
        open_list = {}
        for res in result_json:
            try:
                # mongodb can't use '.' in key
                ip = res.split()[3].replace('.', '_')
                port = res.split()[2]
                if ip in open_list:
                    open_list[ip].append(port)
                else:
                    open_list[ip] = [port]
            except Exception as ex:
                logger.exception(ex.message)
        try:
            if self.store:
                mongo[Config.MONGODB_C_MSCAN].insert({'pid':self.pid, data: open_list})
        except Exception as ex:
            logger.exception(ex.message)

        return open_list


    def scan(self):
        try:
            scan_text = "masscan -p {ports} {target} -oL {output} --randomize-hosts --rate={rate}".format( \
                        ports=self.scan_ports, target=self.scan_ip_range, \
                        output=self.result_file, rate=self.scan_rate)
            os.system(scan_text)
            return self.analysis()
        except Exception as ex:
            logger.exception(ex.message)


    def run(self):
        self.scan()
        self.analysis()
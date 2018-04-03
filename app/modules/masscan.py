#encoding:utf-8 

import os
from datetime import date
from ..lib.core.log import logger
from ..lib.core.config import Config

class MScan(object):

    def __init__(self, pid=-1):
        self.target_file = Config.MSCAN_TARGET_FILE
        self.result_file = Config.MSCAN_RESULT_FILE
        self.rate = Config.MSCAN_RATE
        self.ports = Config.MSCAN_SCAN_PORTS
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
            scan_text = "masscan -p {ports} -iL {target} -oL {output} --randomize-hosts --rate={rate}".format( \
                        (ports=self.ports, target=self.target_file, \
                        output=self.result_file, rate=self.rate))
            os.system(scan_text)
            return self.analysis()
        except Exception as ex:
            logger.exception(ex.message)


    def run(self):
        self.scan()
        self.analysis()
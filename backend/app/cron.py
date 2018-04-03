#encoding:utf-8

import schedule                                                                                                              
import time                                                                                                                  
import os                                                                                                                    
from lib.core.log import logger
from modules.masscan import MScan
from modules.nscan import NScan

def start():                                                                                                                             
    for process_name in psutil.process_iter(attrs=['name']):
        if 'masscan' in process_name.name():
            sign = True

    if not sign:
        mscan = MScan()
        mscan.run()
        nscan = NScan()
        nscan.run()

def job():                                                                                                                   
    start()

                                                                                                                                 
def main():                                                                                                                  
    schedule.every().day.at("00:00").do(job)

    start() # for first run                                                                                                                          
    while True:                                                                                                              
        try:
            schedule.run_pending()                                                                                               
            time.sleep(20)                                                                                                        
            logger.info("Penework is running...")
        except Exception as ex:
            logger.exception(ex.message)


if __name__ == "__main__":                                                                                                   
    main()                   
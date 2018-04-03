#encoding:utf-8 

import sys
import logging 
from config import Config

class Logger(object):  
    def __init__(self):  
        """ 
        initial 
        """  
        logging.addLevelName(20, "NOTICE:")  
        logging.addLevelName(30, "WARNING:")  
        logging.addLevelName(40, "ERROR:")  
        logging.addLevelName(50, "FATAL:")  
        logging.basicConfig(level=logging.DEBUG,  
                format="%(levelname)s %(asctime)s %(filename)s %(message)s",  
                datefmt="%Y-%m-%d %H:%M:%S",  
                filename=Config.LOG_FILE,  
                filemode="a")  
        console = logging.StreamHandler()  
        console.setLevel(logging.DEBUG)  
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(filename)s %(message)s")  
        console.setFormatter(formatter)  
        logging.getLogger("").addHandler(console)  
  
    def debug(self, msg=""):  
        """ 
        output DEBUG level LOG 
        """  
        logging.debug(str(msg))  
  
    def info(self, msg=""):  
        """ 
        output INFO level LOG 
        """  
        logging.info(str(msg))  
  
    def warning(self, msg=""):  
        """ 
        output WARN level LOG 
        """  
        logging.warning(str(msg))  
  
    def exception(self, msg=""):  
        """ 
        output Exception stack LOG 
        """  
        logging.exception(str(msg))  
  
    def error(self, msg=""):  
        """ 
        output ERROR level LOG 
        """  
        logging.error(str(msg))  
  
    def critical(self, msg=""):  
        """ 
        output FATAL level LOG 
        """  
        logging.critical(str(msg))  

logger = Logger()
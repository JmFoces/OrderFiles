#!/usr/bin/python
import sys

import threading
import multiprocessing
import time
from utils.singleton import Singleton
import logging
import logging.handlers

class Logger(Singleton):
    def __init__(self,level=logging.DEBUG):
        self.log = logging.getLogger(__name__)

        self.log.setLevel(level)
        #if level==logging.INFO:
            #self.handler = logging.handlers.SysLogHandler(address='/dev/log')
        #else:
            #self.handler = logging.StreamHandler()
        #self.handler = logging.StreamHandler()
        self.handler = logging.FileHandler("./organizer.log")

        self.formatter = logging.Formatter('%(asctime)s %(process)d %(levelname)s: %(module)s.%(funcName)s: %(message)s')
        self.handler.setFormatter(self.formatter)

        self.log.addHandler(self.handler)


log = Logger().log
# log.debug("log Instanciated")


def log_cmd(cmd):
    log.debug(cmd.stdout)
    log.error(cmd.stderr)


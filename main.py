#!/usr/bin/python
# -*- coding: utf-8
import sys
import os
from os import listdir
from utils.log import log
from mtypes.creators.file_factory import FileFactory
from multiprocessing import Process
from threading import Thread
from constants import WORK_DIR


from utils.order.organizer import Organizer

import time

EXCLUDE_ROOT=[ "debian", "pypi" , "clamav", "linux-malware-detector", "roundcubemail", "hp" ,"debian_repo", "debian_security"]
ROOT_CONCURRENCY = 4

def work(path):
    ffactory = FileFactory()
    organizer = Organizer()
    mfile = ffactory.create_file(path)
    organizer.organize(mfile)

if __name__ == "__main__":
    procs = []
    for param in sys.argv[1:]:
        try:
            if param not in EXCLUDE_ROOT :
                if os.path.isdir(param):
                    for subdir in listdir(param):
                        if subdir not in EXCLUDE_ROOT:
                            p = Process(target=work, args=[os.path.join(param, subdir)])
                            procs.append(p)
                else:
                    p = Process(target=work, args=[param])
                    procs.append(p)
        except Exception,e:
            log.exception(e)

    for p in procs:
        log.info("Starting proc {0}".format(p.pid))
        p.start()
        log.info("waiting for proc {0}".format(p.pid))

    while len(procs) > 0:
        log.info("Pending tasks {0} ".format(len(procs)))
        for p in procs:
            p.join(timeout=10)
            if not p.is_alive():
                log.info("Ended task {0}".format(p.pid))
                procs.remove(p)
                break
    log.info("Finished all tasks")

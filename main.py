#!/usr/bin/python3
# -*- coding: utf-8
import sys
import os
from os import listdir
from utils.log import log
from mtypes.creators.file_factory import FileFactory
from multiprocessing import Pool, Process
from config import EXCLUDE_ROOT
from utils.order.organizer import Organizer
from hachoir.core import config
config.quiet = True
## FROM: https://stackoverflow.com/questions/6974695/python-process-pool-non-daemonic


class NoDaemonProcess(Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)
    
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)



class NonDaemonsPool(Pool):
    Process = NoDaemonProcess


def work(path):
    log.info("Working {}".format(path))
    ffactory = FileFactory()
    organizer = Organizer()
    mfile = ffactory.create_file(path)
    organizer.organize(mfile)
    log.info("Finished {}".format(path))
    return path


if __name__ == "__main__":
    ppool = NonDaemonsPool()
    result_list = []

    for param in sys.argv[1:]:
        try:
            result_list.append(ppool.apply_async(work, args=(param,)))
        except Exception as e:
            log.exception(e)

    for result in result_list:
        log.info("Finished  {}".format(result.get()))

    ppool.close()
    ppool.join()
    log.info("Finished all tasks")

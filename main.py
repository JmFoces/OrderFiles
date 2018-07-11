#!/usr/bin/python3
# -*- coding: utf-8
import sys
import os
from os import listdir
from queue import Queue

from utils.log import log
from mtypes.creators.file_factory import FileFactory
import multiprocessing
from multiprocessing import Process
from config import EXCLUDE_ROOT
from utils.order.organizer import Organizer
from hachoir.core import config
config.quiet = True


def work(path):
    ffactory = FileFactory()
    organizer = Organizer()
    mfile = ffactory.create_file(path)
    organizer.organize(mfile)

work_queue = Queue()
def worker_loop():
    path = work_queue.get()
    log.info("Ordering {}".format(path))
    work(path)
    log.info("Finished {}".format(path))


if __name__ == "__main__":

    for param in sys.argv[1:]:
        try:
            p = Process(target=work, args=(param,))
            p.start()
            p.join()
        except Exception as e:
            log.exception(e)

    log.info("Finished all tasks")
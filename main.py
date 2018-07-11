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
    procs = []

    for i in range(0, multiprocessing.cpu_count()):
        p = Process(target=worker_loop)
        procs.append(p)

    for param in sys.argv[1:]:
        try:
            work_queue.put(param)
        except Exception as e:
            log.exception(e)

    for p in procs:
        p.start()

    work_queue.join()
    for p in procs:
        p.terminate()
    log.info("Finished all tasks")
#!/usr/bin/python3
# -*- coding: utf-8
import sys
import os
from os import listdir
from utils.log import log
from mtypes.creators.file_factory import FileFactory
from multiprocessing import Pool, TimeoutError
from config import EXCLUDE_ROOT
from utils.order.organizer import Organizer
from hachoir.core import config
config.quiet = True

def work(path):
    log.info("Working {}".format(path))
    ffactory = FileFactory()
    organizer = Organizer()
    mfile = ffactory.create_file(path)
    organizer.organize(mfile)
    log.info("Finished {}".format(path))


if __name__ == "__main__":
    ppool = Pool()

    for param in sys.argv[1:]:
        try:
            ppool.apply_async(work, (param))
        except Exception as e:
            log.exception(e)

    ppool.join()
    log.info("Finished all tasks")

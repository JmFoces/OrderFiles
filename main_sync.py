#!/usr/bin/python3
# -*- coding: utf-8
import sys
import os
from os import listdir
from utils.log import log
from mtypes.creators.file_factory import FileFactory
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


if __name__ == "__main__":
    procs = []
    for param in sys.argv[1:]:
        try:
            if param not in EXCLUDE_ROOT :
                work(param)
        except Exception as e:
            log.exception(e)

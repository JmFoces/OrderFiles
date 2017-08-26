#!/usr/bin/python
import os
import sh
from utils.log import log
WORK_DIR="/srv/orderedfiles"
INDEX_PATH = os.path.join(WORK_DIR, "index")

HOSTNAME = sh.hostname().stdout.replace("\n", "")


SOURCEFOLDER_CONTENTS=[
    "^\.idea$",
    "^main.py$",
    "^manage.py$",
    "^main.c$",
    "^manage.py$",
    "^main.cpp$",
    "^.metadata$",
    "^\.git$",
    "^\.svn$",
    "^\.svn-base$",
    "^\.project$",
    "^include$",
    "^src$",
    "^debug$",
    "^Classes$",
    "^.*\.xcodeproj$"
]
PROJECTNAMES=["int_net", "inet", "L2L3Forwarder", "Rehtse"]

BANNED_MIMES = [
    "application/java-archive",
    "application/vnd.debian.binary-package"
]
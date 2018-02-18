#!/usr/bin/python
import sh

HOSTNAME = str(sh.hostname().stdout,'utf8').replace("\n", "")


SOURCEFOLDER_CONTENTS = [
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


import os
import re
import sh
import json

from mtypes.file.container.mapable_drive import MapableDrive
from utils.exceptions import *
from mtypes.file.container import Container
from mtypes.file.container.filesystem import FileSystem
from utils.log import log


class LVM(MapableDrive):
    # Represents a partition table.
    # LSBLK_KEYS = "NAME,FSTYPE,UUID"
    
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        Container.__init__(self, path, magic_str=magic_str, mime_type=mime_type, metadata=metadata, parent=parent)
        self.lodev = None
        self.children = set()
        self.vgname=""
        log.debug("Created Mapable Drive Container File {0}".format(self.path))

    def load(self):
        self.vgname = sh.pvdisplay(self.path, "-C").stdout
        self.vgname = self.vgname.split(b"\n")[1].split(b" ")[4]
        self.vgname = str(self.vgname,'utf8')
        sh.vgchange("-ay", self.vgname)
        return super(LVM, self).load()

    def unload(self):
        sh.vgchange("-an", self.vgname)
        return super(LVM, self).unload()

    def process_devicemap(self):
        return super(LVM, self).process_devicemap()

    def process_sub_devicemap(self, children):
        return super(LVM, self).process_sub_devicemap(children)

    def get_children(self):
        return super(LVM, self).get_children()

    def __str__(self):
        return "LVM{0}".format(self.path)

    def get_ordered_path(self):
        return super().get_ordered_path()

    def gen_ordered_paths(self):
        return super().gen_ordered_paths()



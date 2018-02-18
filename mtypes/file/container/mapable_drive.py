import os
import re
import sh
import json
from utils.exceptions import *
from mtypes.file.container import Container
from mtypes.file.container.filesystem import  FileSystem
from utils.log import log


class MapableDrive(Container):
    # Represents a partition table.
    #LSBLK_KEYS = "NAME,FSTYPE,UUID"
    LSBLK_KEYS = "NAME"
    RECURSION_STOP_MSG = "Mappable drive End Recursion condition reached"

    def __init__(self, path, magic_str=None, mime_type=None, metadata=None,parent=None):
        Container.__init__(self, path, magic_str, mime_type, metadata, parent)
        self.lodev = None
        self.children = set()
        log.debug("Created Mapable Drive Container File {0}".format(self.path))

    def load(self):
        log.debug("loading mapable drive {0}".format(self.path))
        try:
            if not re.search(r"block special", str(sh.file(self.path).stdout,'utf8'), flags=re.IGNORECASE):
                self.lodev = sh.losetup("-f").split()[0]
                sh.losetup(self.lodev, self.path)
                sh.blkid(self.lodev)
                try:
                    sh.partprobe(self.lodev)
                except:
                    pass
            else:
                sh.blkid(self.path)
                try:
                    sh.partprobe(self.path)
                except:
                    pass
            sh.sync("/dev/")
            self.process_devicemap()
        except Exception as e:
            log.exception(e)
            return False
        return True

    def unload(self):
        try:
            if self.lodev:
                sh.losetup("-d", self.lodev)
            try:
                sh.partprobe(self.lodev)
                sh.rm("{0}p*".format(self.lodev))
            except:
                pass
            self.children=[]
            sh.sync("/dev/")
            return True
        except sh.ErrorReturnCode:
            sh.sync("/dev/")
            return False

    def process_devicemap(self):
        if self.lodev:
            dev_path = self.lodev
        else:
            dev_path = self.path
        root = json.loads(str(sh.lsblk("-pJ", "-o", self.LSBLK_KEYS, dev_path).stdout,'utf8'))["blockdevices"][0]
        try:
            self.process_sub_devicemap(root["children"])
        except KeyError:
            log.debug(self.RECURSION_STOP_MSG)

    def process_sub_devicemap(self, children):
        if isinstance(children,list):
            for child in children:
                self.process_sub_devicemap(child)
        elif isinstance(children,dict):
            dev = children.pop("name")
            if dev != self.path:
                self.children.add(str(dev))
            try:
                for item in children["children"]:
                    self.process_sub_devicemap(item)
            except KeyError:
                log.debug(self.RECURSION_STOP_MSG)

    def get_children(self):
        child_output = list(self.children)
        log.debug("{0} children: {1} ".format(self, child_output))
        return child_output

    def __str__(self):
        return "MapableDrive{0}".format(self.path)

    def get_ordered_path(self):
        return Container.get_ordered_path(self)


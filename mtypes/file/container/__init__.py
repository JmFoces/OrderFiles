import os
import sh
import random
from mtypes.file import File
from utils.log import log
from config import WORK_DIR


class Container(File):
    # Represents a container. Anything that may have embed files (rar,tgz,ext4...)
    META_PATH_GENERATORS = []
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None,parent=None):
        File.__init__(self, path, magic_str, metadata,mime_type)
        log.debug("Created Container File {0}".format(self.path))
        self.output_path = None
        self.loaded = False
        
    def load(self):
        """
            Must be implemented by all containers.
            It dumps all content on the output path
        :return:
        """
        raise NotImplemented()

    def unload(self):
        """
            Must be implemented by all containers.
            It dumps all content on the output path
        :return:
        """
        raise NotImplemented()

    def get_children(self):
        if not self.output_path:
            path = self.path
        else:
            path = self.output_path
        #log.debug("Getting children from path {0}".format(path))
        return str(sh.find(path, "-maxdepth", "1", "!", "-name", "lost+found").stdout, 'utf8').split("\n")[1:-1]

    def get_all_children(self, filter=()):
        if not self.output_path:
            path = self.path
        else:
            path = self.output_path
        return str(sh.find(path, filter).stdout,'utf8').split("\n")[1:-1]

    def __str__(self):
        return "{0} @ {1}".format(self.path, self.output_path)

    def create_output_path(self):
        if not self.output_path:
            sh.mkdir("-p", WORK_DIR)
            sh.chmod("700", WORK_DIR)
            self.output_path = str(sh.mktemp("-p", WORK_DIR, "-d").stdout, 'utf8').split("\n")[0]
            log.debug("Output path -> {0}".format(self.output_path))
            sh.chmod("700",self.output_path)

    def get_ordered_path(self):
        return File.get_ordered_path(self)
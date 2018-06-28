import os
from mtypes.file import File
from utils.log import log



class Data(File):
    # Represents a file that does not contain embed files.
    META_PATH_GENERATORS = []
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        File.__init__(self, path, magic_str, mime_type, metadata, parent)
        #log.debug("Created Data File {0}".format(self.path))

    def get_children(self):
        return []

    def __str__(self):
        return "Data:{0}".format(self.path)

    def get_ordered_path(self):
        return File.get_ordered_path(self)

    def gen_ordered_paths(self):
        File.gen_ordered_paths(self)
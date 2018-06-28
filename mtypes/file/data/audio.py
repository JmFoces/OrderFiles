import os

from mtypes.file.data import Data
from utils.log import log
from utils.order.meta_path_composer import get_author, get_album


class Audio(Data):

    META_PATH_GENERATORS = [get_author, get_album]

    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        Data.__init__(self, path, magic_str, mime_type, metadata, parent)

        #log.debug("Created Data File {0}".format(self.path))

    def get_children(self):
        return []

    def __str__(self):
        return "Audio:{0}".format(self.path)

    def get_ordered_path(self):
        return Data.get_ordered_path(self)

    def gen_ordered_paths(self):
        return Data.gen_ordered_paths(self)
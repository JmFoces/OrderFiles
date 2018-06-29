from mtypes.file.data import Data
from utils.log import log


class Text(Data):

    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        Data.__init__(self, path, magic_str, mime_type, metadata, parent)
        #log.debug("Created Data File {0}".format(self.path))

    def get_children(self):
        return []

    def __str__(self):
        return "Text:{0}".format(self.path)

    def get_ordered_path(self):
        return super().get_ordered_path()

    def gen_ordered_paths(self):
        return super().gen_ordered_paths()

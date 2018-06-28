import os
import sh
from config import WORK_DIR
from utils.log import log

class File:
    # Base File Class
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        if not path or not os.path.exists(path):
            if not os.path.islink(path):
                #If it isn't a symlink then fail.
                raise Exception("Unable to create file without a path {0} {1}".format(path, path.__class__))
        self.magic_str = magic_str
        self.mime_type = mime_type
        self.path = path
        self.metadata = metadata
        self.parent=None
        #log.debug("Created File {0}".format(self.path))

    def get_children(self):
        return []
        
    def get_root_parent(self):
        if self.parent==None:
            return self
        else:
            return self.parent.get_root_parent()

    def load(self):
        pass

    def unload(self):
        pass

    def get_ordered_path(self):
        try:
            ordered_folder = str(self.mime_type, 'utf8') if isinstance(self.mime_type, bytes) else self.mime_type
            ordered_folder = os.path.join(WORK_DIR, ordered_folder)
        except (TypeError, AttributeError):
            ordered_folder = "NoMime"
            ordered_folder = os.path.join(WORK_DIR, ordered_folder)
        sh.mkdir("-p", ordered_folder)
        return ordered_folder

    def gen_ordered_paths(self):
        pass

    def __str__(self):
        return "File:{0}".format(self.path)

    def __repr__(self):
        return "File(%s)" % self.path

    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def is_source_container(self):
        return False
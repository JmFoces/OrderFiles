import os
import re
from mtypes.file.container import Container
from constants import SOURCEFOLDER_CONTENTS
from config import PROJECTNAMES
from utils.log import log


class Directory(Container):

    # Represents a directory container
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        Container.__init__(self, path, magic_str, mime_type, metadata, parent)
        #log.debug("Created Directory Container File {0}".format(self.path))

    def __str__(self):
        return "Directory:{0}".format(self.path)

    def load(self):
        return True

    def unload(self):
        return True

    def get_ordered_path(self):
        return super().get_ordered_path()

    def gen_ordered_paths(self):
        return super().gen_ordered_paths()


    def is_source_container(self):
        children = self.get_children()
        for projname in PROJECTNAMES:
            if re.search("{0}".format(projname), os.path.basename(self.path), flags=re.IGNORECASE):
                try:
                    log.debug("{0} Is source Projname".format(self.path))
                except UnicodeError:
                    pass
                return True
        for check in SOURCEFOLDER_CONTENTS:
            for child in children:
                if re.search("{0}".format(check), os.path.basename(child)):
                    try:
                        log.debug("{0} Is source child name {1} ".format(self.path,child))
                    except UnicodeError:
                        pass
                    return True

        return False
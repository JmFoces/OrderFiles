import re
from utils.log import log
from mtypes.file import File
from utils.command import launch_command
import sh

class Pointer(File):
    # Represents a symbolic link

    def __init__(self, path, magic_str=None, mime_type=None,parent=None):
        File.__init__(self, path, magic_str, mime_type, parent)
        retcode, stdout, stderr = launch_command("readlink -e {0}".format(self.path))
        self.ptr = stdout.strip()
        if "proc/self" in self.ptr or "dev/pts" in self.ptr:
            ## Protect access over self fds (stdin stdout stderr)
            self.ptr = "/dev/null"
        log.debug("Created Pointer File to {0}".format(self.ptr))

    def get_children(self):
        return [self.ptr]

    def get_all_children(self, filter=()):
        return self.get_children()

    def __str__(self):
        return "Pointer:{0} --> {1}".format(self.path,self.ptr)
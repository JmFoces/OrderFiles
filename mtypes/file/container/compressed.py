

import sh
from mtypes.file.container import Container
from utils.log import log
from subprocess import Popen
import subprocess
import time
import pexpect


class Compressed(Container):

    # Represents a compressed container. (rar,tar,gz,zip...)
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        Container.__init__(self, path, magic_str=magic_str, mime_type=mime_type, metadata=metadata, parent=parent)
        #log.debug("Created Compressed Container File {0}".format(self.path))

    def load(self):
        self.create_output_path()
        try:

            #patoolib.extract_archive(self.path, outdir=self.output_path, interactive=False)
            #p = Process(target=patoolib.extract_archive,kwargs={"archive":self.path, "outdir":self.output_path, "interactive":False})
            command="patool --non-interactive extract --outdir {0} {1}".format(self.output_path, self.path)
            child = pexpect.spawn(command)
            while True:
                #stdout, stderr = cmd_proc.communicate(input=bytes("\n", 'utf8'), timeout=10)
                child.sendline("")
                if child.isalive():
                    time.sleep(1)
                else:
                    break

            if child.exitstatus == 0:
                return True
            else:
                self.unload()
                return False
        except Exception as e:
            err_str = "Unable to unpack {0} @ ".format(self.path,self.output_path)
            log.error(err_str)
            log.exception(e)
            return False

    def unload(self):
        try:
            sh.rm("-rf", self.output_path)
            return True
        except sh.ErrorReturnCode:
            return False

    def __str__(self):
        return "Compressed:{0}".format(self.path)

    def get_ordered_path(self):
        return super().get_ordered_path()

    def gen_ordered_paths(self):
        return super().gen_ordered_paths()

    def create_output_path(self):
        Container.create_output_path(self)
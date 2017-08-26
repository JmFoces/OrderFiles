
import os
import sh
from utils.exceptions import UnableToLoad
import patoolib
from mtypes.file.container import Container
from utils.log import log
from subprocess import Popen
import subprocess
import time
from threading import Thread

def write_newline_onpipe(pipe):
    try:
        for i in range(0, 20):
            pipe.write("\r\n")
            pipe.flush()
            time.sleep(0.25)
    except:
        pass


class Compressed(Container):

    # Represents a compressed container. (rar,tar,gz,zip...)
    def __init__(self, path, magic_str=None, mime_type=None, metadata=None, parent=None):
        Container.__init__(self, path, magic_str, mime_type, metadata, parent)
        #log.debug("Created Compressed Container File {0}".format(self.path))

    def load(self):
        self.create_output_path()
        try:

            #patoolib.extract_archive(self.path, outdir=self.output_path, interactive=False)
            #p = Process(target=patoolib.extract_archive,kwargs={"archive":self.path, "outdir":self.output_path, "interactive":False})
            command="patool --non-interactive extract --outdir {0} {1}".format(self.output_path, self.path)
            cmd_proc = Popen(command,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             executable="/bin/bash"
                             )
            writer = Thread(target=write_newline_onpipe,args=[cmd_proc.stdin])
            writer.start()

            stdout, stderr = cmd_proc.communicate(input="\r\n")
            log.debug("PATOOL: {0} , {1}".format(stdout, stderr))
            if cmd_proc.returncode == True:
                return True
            else:
                self.unload()
                return False
        except Exception, e:
            err_str = "Unable to unpack {0} @ ".format(self.path,self.output_path)
            log.error(err_str)
            #log.exception(e)
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
        return Container.get_ordered_path(self)

    def create_output_path(self):
        Container.create_output_path(self)
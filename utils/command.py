import re
import sys
import os
from subprocess import Popen
import subprocess
from utils.log import log


def launch_command(command, unsafe=True):
    log.debug("commmand {0}".format(command))
    cmd_proc = Popen(command,
                     shell=unsafe,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     executable="/bin/bash"
                     )
    stdout, stderr = cmd_proc.communicate()
    return cmd_proc.returncode, stdout, stderr


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def launch_interactive_command(command, unsafe=True):
    return subprocess.call(
        command,
        shell=unsafe,
        executable="/bin/bash"
    )



def demote(user):
    ret, stdout, stderr = launch_command("getent passwd | grep '{0}'".format(user))
    uid=int(stdout.split(":")[2],10)
    gid=int(stdout.split(":")[3],10)
    def preexec_hook():
        log.debug("Demoting process {0}".format(os.getpid()))
        os.setuid(uid)
        
    return preexec_hook
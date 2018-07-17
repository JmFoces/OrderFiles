import sh
import os
import re

import config
import constants
from utils.exceptions import *
from utils.command import *


class Index:
    INDEX_PATH = config.INDEX_PATH
    DEPTH = 2

    def __init__(self):
        self.tmp = os.path.join(self.INDEX_PATH, "tmp")
        sh.mkdir("-p", self.tmp)
        self.step = 2

    def put_file(self, path):
        temp_file = str(sh.mktemp("-p", self.tmp).stdout,'utf8').strip()
        path = path.strip()
        if "'" in path:
            returncode, stdout, stderr = launch_command(
                "dd if=\"{0}\" iflag=nofollow bs=4k | tee {1} | sha1sum".format(
                    path,
                    temp_file
                )
            )
        else:
            returncode, stdout, stderr = launch_command(
                "dd if='{0}' iflag=nofollow bs=4k | tee {1} | sha1sum".format(
                    path,
                    temp_file
                )
            )
        if returncode != 0:
            print(stdout)
            print(stderr)
            raise UnableToHashFile("File : {0}".format(path))
        hash_str = re.search("^[0-9a-f]*", str(stdout,'utf8')).group(0)
        destination_folder = self.create_destination_folder(hash_str)
        destination_path = os.path.join(destination_folder, hash_str)
        if not self.is_stored(hash_str):
            sh.mv(temp_file, destination_path)
            sh.chmod("444", destination_path)
        else:
            sh.rm(temp_file)
        return destination_path

    def create_destination_folder(self, hash_str):
        count = 0

        path = self.INDEX_PATH
        while count < self.DEPTH:
            path = os.path.join(path, hash_str[count:count+self.step])
            sh.mkdir("-p", path)
            count += self.step
        return path

    def is_stored(self, hash_str):
        count = 0

        path = self.INDEX_PATH
        while count < self.DEPTH:
            path = os.path.join(path, hash_str[count:count + self.step])
            count += self.step
        path = os.path.join(path, hash_str)
        return os.path.exists(path)


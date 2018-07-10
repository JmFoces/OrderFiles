import stat

import hachoir
import magic
import os
import sh
import re

from utils.log import log
from utils.exceptions import *
from mtypes.file.data import Data
from mtypes.file.data.audio import Audio
from mtypes.file.data.document import Document
from mtypes.file.data.image import Image
from mtypes.file.data.text import Text
from mtypes.file.data.video import Video
from mtypes.file.container.directory import Directory
from mtypes.file.container.compressed import Compressed
from mtypes.file.container.filesystem import FileSystem
from mtypes.file.container.mapable_drive import MapableDrive
from mtypes.file.pointer import Pointer
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def distinguish_dos_from_fs(path, magic_str=None, mime_type=None, metadata=None, parent=None):
    ## Must have the same header than File.__init__
    cmd = str(sh.blkid("-o", "export", path).stdout,'utf8')
    if re.search("\nTYPE=.*\n", cmd):
        return FileSystem(path, magic_str,parent)
    else:
        return MapableDrive(path, magic_str,parent)

def get_metadata(full_name):
    metadata = None
    try:
        parser = createParser(full_name)
        metadata = extractMetadata(parser)
        if parser:
            parser.stream._input.close()
            del parser
    except hachoir.stream.input.InputStreamError:
        ## is directory
        metadata = None
    except Exception as err:
        log.exception(err)
        log.error("Cannot extract metadata")
        metadata = None
    finally:
        return metadata

class FileFactory:
    CONTAINER_TYPES_MAP = {
        ## Regex : Concrete type
        "symbolic link": Pointer,
        "directory$": Directory,
        '.*NTFS,.*serial number': FileSystem,
        'POSIX tar archive': Compressed,
        '(?!not) compressed': Compressed,
        'compressed': Compressed,
        'filesystem': FileSystem,
        "DOS/MBR boot sector": distinguish_dos_from_fs,
        "partition table": MapableDrive,
        " lvm": MapableDrive,
        "LVM2 PV .*": MapableDrive
    }
    MIME_TYPES_MAP = {
        ".*zip.*": Compressed,
        ".*zlib": Compressed,
        "application/x-tar": Compressed,
        "application/x-rar": Compressed,
        "application/x-lzma": Compressed,
        "application/x-7z-compressed": Compressed,
        "application/vnd.ms-opentype": Document,
        "application/vnd.ms-excel": Document,
        "application/vnd.ms-powerpoint": Document,
        "application/vnd.ms-excel": Document,
        "application/pdf": Document,
        "application/.*": Data,
        "audio/.*" : Audio,
        "image/.*": Image,
        "text/.*" : Text,
        "video/.*": Video,
        "inode/.*": None
    }
    MAGIC = magic.Magic(flags=magic.MAGIC_DEVICES)
    MAGIC_MIME = magic.Magic(flags=magic.MAGIC_MIME_TYPE)

    def __init__(self):
        self.tmp_file_obj_set = None

    def get_file_magic(self, path):
        try:
            dat_file = open(path, 'rb')
            raw = dat_file.read(1024 * 10)
            dat_file.close()
            magic_str = self.MAGIC.id_buffer(raw)
            mime_str = self.MAGIC_MIME.id_buffer(raw)
        except IOError:
            try:
                magic_str = self.MAGIC.id_filename(path)
                mime_str = self.MAGIC_MIME.id_filename(path)
            except IOError:
                return "", ""
        #log.debug("{0} has magic : {1} ".format(path, magic_str))
        return magic_str, mime_str

    def create_file(self, path, parent=None):
        file_obj = None
        #if stat.S_ISFIFO(os.stat(path).st_mode) or stat.S_ISCHR(os.stat(path).st_mod):
        if stat.S_ISFIFO(os.stat(path).st_mode) or stat.S_ISCHR(os.stat(path).st_mode):
            return None

        magic_str, mime_str = self.get_file_magic(path)
        metadata = get_metadata(path)

        for regex, file_class in self.CONTAINER_TYPES_MAP.items():
            if file_class and re.search(regex, magic_str, flags=re.IGNORECASE) :
                try:
                    file_obj = file_class(path, magic_str=magic_str, mime_type=mime_str, metadata=metadata, parent=parent)
                    break
                except IncompatibleFS:
                    log.error("Attempted to create filesystem from block device without success")
                    pass

        if not file_obj:
            for regex, file_class in self.MIME_TYPES_MAP.items():
                if file_class and re.search(regex, mime_str, flags=re.IGNORECASE):
                    try:
                        file_obj = file_class(path, magic_str=magic_str, mime_type=mime_str, metadata=metadata, parent=parent)
                        break
                    except Exception as e:
                        log.exception(e)
                        pass

        if not file_obj:
            file_obj = Data(path, magic_str)

        return file_obj

    def _load_create_children_of(self, file_obj, parent_type, children_type,parent=None):
        file_obj.load()
        for child_path in file_obj.get_children():
            self.tmp_file_obj_set = self.tmp_file_obj_set.union(
                self.create_file_children_of(
                    child_path,
                    parent_type,
                    children_type
                )
            )

    def create_file_children_of(self, path, parent_type=MapableDrive, children_type=FileSystem, parent=None):
        self.tmp_file_obj_set = set()
        file_obj = self.create_file(path,parent)
        if not parent_type or isinstance(file_obj, parent_type):
            self._load_create_children_of(file_obj, parent_type, children_type,parent=file_obj)
        if not children_type or isinstance(file_obj, children_type):
            self.tmp_file_obj_set.add(file_obj)

        return self.tmp_file_obj_set


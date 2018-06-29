import os
import time
import sh
import json
import re
from utils.command import launch_command
from utils.exceptions import *
from utils.log import log, log_cmd
from mtypes.file.container import Container


class FileSystem(Container):
    # Represents a filesystem container. (ext4,ext3,fat...)
    SUPPORTED_FS = [
        "ext2",
        "ext3",
        "ext4",
        "exfat",
        "vfat",
        "ntfs",
        "fat32",
        "fat",
        "msdos"
    ]
    MAX_ATTEMPTS = 2
    MOUNT_OPTIONS = "nodev,noexec,nosuid"
    LSBLK_KEYS = "FSTYPE,UUID,LABEL"

    def __init__(self, path, magic_str=None, mime_type=None, metadata=None,parent=None):
        Container.__init__(self, path, magic_str, mime_type, metadata, parent)
        attempt = 0
        self.fstype = None
        self.label = None
        self.uuid = None
        while attempt < self.MAX_ATTEMPTS:
            try:
                if self.set_fsattrs():
                    break
            except IncompatibleFS:
                time.sleep(1)
                pass
            finally:
                attempt += 1
        log.debug("Created Filesystem Container file {0}".format(self))

    def set_fsattrs(self):
        log.debug("Getting filesystem attributes {0}".format(self.path))
        try:
            me = json.loads(str(sh.lsblk("-pJ", "-o", self.LSBLK_KEYS, self.path).stdout,'utf8'))["blockdevices"][0]
            try:
                self.uuid = me["uuid"]
                log.debug("GOT UUID: {0}".format(self.uuid))
            except KeyError:
                self.uuid = None
            try:
                self.fstype = me["fstype"]
                log.debug("GOT FSTYPE: {0}".format(self.fstype))
            except KeyError:
                self.fstype = None

            try:
                self.label = me["label"]
            except KeyError:
                self.label = None

        except sh.ErrorReturnCode_32:
            # Not a block device falling back to blkid
            cmd = str(sh.blkid("-o", "export", self.path).stdout,'utf8')
            try:
                self.uuid = re.search("UUID=(.*)", cmd).group(1)
            except (TypeError, AttributeError):
                self.uuid = None
            try:
                self.fstype = re.search("TYPE=(.*)", cmd).group(1)
            except (TypeError, AttributeError):
                self.fstype = None
            try:
                self.label = re.search("LABEL=(.*)", cmd).group(1)
            except (TypeError, AttributeError):
                self.label = None

        if str(self.fstype) not in self.SUPPORTED_FS:
            log.error("{0} is out of {1} : {2}".format(self.fstype, self.SUPPORTED_FS, self.path))
            raise IncompatibleFS("Not working with {0} fstype {1}".format(self.path, self.fstype))
        return True

    def mount_compat(self,mode="ro"):
        status=True

        try:
            sh.mount("-o", "{0},{1}".format(mode, self.MOUNT_OPTIONS), self.path, self.output_path)
        except sh.ErrorReturnCode as e:
            log.debug("Legacy re-mount opts for {0}".format(self)) 
            try:
                sh.mount("-o", "{0}".format(mode), self.path, self.output_path)
            except:
                try:
                    sh.mount(self.path, self.output_path)
                except Exception as e :
                    log.error("Cannot mount : {0}".format(self))
                    log.exception(e)
                    status=False
        return status

    def load(self, mode="ro"):
        try:
            self.create_output_path()
            sh.chmod("700", self.output_path)
        except sh.ErrorReturnCode as e:
            ## Already mounted readonly.
            pass
        try:
            log.debug("Loading {0}".format(self))
        
            self.loaded = self.mount_compat("rw")
            if self.loaded:
                try:
                    sh.rm("-rf",
                        os.path.join(self.output_path,'._.Trashes'),
                        os.path.join(self.output_path,'.Spotlight-V100'),
                        os.path.join(self.output_path,'lost+found'),
                        os.path.join(self.output_path,'$RECYCLE.BIN'),
                        os.path.join(self.output_path,'System Volume Information')
                    )
                except:
                    pass
                try:
                    sh.umount(self.output_path)
                except:
                    self.loaded=False
                self.loaded = self.mount_compat(mode)
                return self.loaded
            else:
                return False
        except sh.ErrorReturnCode as e:
            self.unload()
            log.exception(e)
            return False

    def unload(self):
        log.debug("Unloading {0}".format(self))
        try:
            sh.umount("-lf", self.path)
        except sh.ErrorReturnCode:
            pass
        try:
            sh.rm("-rf",self.output_path)
        except sh.ErrorReturnCode:
            return False
        self.loaded = False
        return True

    @classmethod
    def agro_mkfs_ext4(cls,dev_path):
        return launch_command("mkfs.ext4 -F -O^has_journal -E lazy_itable_init=0 {0}".format(dev_path))
        
    def regenerate(self):
        if re.search("ext[2-4]!?",self.fstype):
            log.debug("Formatting ext4")
            returncode, stdout, stderr = launch_command("mkfs.ext4 -F -O^has_journal -E lazy_itable_init=0 {0}".format(self.path))
            
        elif re.search("fat",self.fstype):
            log.debug("Formatting FAT")
            
            returncode, stdout, stderr = launch_command("mkfs.fat {0}".format(self.path))
            if returncode != 0:
                returncode, stdout, stderr = launch_command("mkfs.fat -I {0}".format(self.path))

        else:
            log.debug("Formatting NTFS")
            returncode, stdout, stderr = launch_command("mkfs.ntfs -Ff {0}".format(self.path))
        return returncode, stdout, stderr

    def __str__(self):
        return "Filesystem {0} mounted @ {1}".format(self.path, self.output_path)

    def get_ordered_path(self):
        return super().get_ordered_path()

    def gen_ordered_paths(self):
        return super().gen_ordered_paths()

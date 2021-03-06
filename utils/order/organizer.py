import os

import re
import sh
import sys
import logging
from config import WORK_DIR, SW_PROJECTS_OUTPUT, METAFPATHFILE
from utils.order.meta_path_composer import run_path_update
from utils.log import log
from utils.order.index import Index
from mtypes.creators.file_factory import FileFactory
from multiprocessing import Process, Manager

SOURCEFOLDER_ORDERED="Project"



class Organizer:
    def __init__(self):
        self.ffactory = FileFactory()
        self.index = Index()

    def dive(self, mfile):
        for child in mfile.get_children():
            log.debug("Organizing child {1} of {0}".format(mfile, child))
            child_file = self.ffactory.create_file(child)
            if child_file:
                self.organize(child_file, False)
            else:
                logging.debug("Bypassed {}".format(child))
            #sys.stdout.flush()

    def organize(self, mfile, root_call=True):
        loaded_mfiles = set()

        if root_call:
            log.info("Organizing {0}".format(mfile))
        try:
            if mfile.load():
                log.info("Organizing childs of {0}".format(mfile))
                if mfile.is_source_container():
                    log.debug("{0} is source".format(mfile.path))
                    dump_dir_path = os.path.join(WORK_DIR, SW_PROJECTS_OUTPUT)
                    sh.mkdir("-p", dump_dir_path)

                    dump_dir_path = sh.mktemp(
                        "-d",
                        "-p",
                        dump_dir_path,
                        "--suffix",
                        os.path.basename(
                            mfile.path
                            )
                        ).stdout.strip()
                    try:
                        sh.rsync("-rat", mfile.path, dump_dir_path)
                    except sh.ErrorReturnCode_23:
                        ## Rsync errs related with attrs or others
                        pass

                else:
                    loaded_mfiles.add(mfile)
                    #self.dive(mfile)
                    p = Process(target=Organizer.dive, args=[self, mfile])
                    p.start()
                    p.join()
            else:
                destination_path = self.index.put_file(mfile.path)
                metapath_file = open("{}.{}".format(destination_path, METAFPATHFILE), 'ab')
                metapath_file.write(bytes(mfile.path + "\n", 'utf8'))
                metapath_file.close()
                try:
                    ordered_path = mfile.get_ordered_path()
                    sh.mkdir("-p", os.path.join(ordered_path,'NoMeta'))
                    fname = os.path.basename(mfile.path)
                    destination_fname = os.path.basename(destination_path)
                    for link in mfile.gen_ordered_paths():
                        log.debug("{} to {}".format(mfile.path,link))
                        sh.mkdir("-p", link)
                        try:
                            has_ext = re.search(r"(\..*)", fname)
                            extension = has_ext.group(1)
                            link = os.path.join(
                                link,
                                u"{0}{1}".format(destination_fname, extension))
                        except AttributeError:
                            link = os.path.join(
                                link,
                                u"{0}".format(destination_fname))
                        log.info(u"File {0} @ {1}".format(str(mfile), ordered_path))
                        sh.ln("-s", destination_path, link)
                except sh.ErrorReturnCode_1:
                    pass
                except sh.ErrorReturnCode as e:
                    log.exception(e)
        except Exception as e:
            log.error("Organizer error {0}".format(mfile.path))
            log.exception(e)
        finally:
            for loaded_mfile in loaded_mfiles:
                try:
                    loaded_mfile.unload()
                except Exception as  e:
                    log.error("Error unloading {0}".format(mfile.path))
                    log.exception(e)
            return True

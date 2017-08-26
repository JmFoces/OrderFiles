import os
import sh
import sys
from constants import WORK_DIR
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
            self.organize(child_file, False)
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
                    dump_dir_path = os.path.join(WORK_DIR, "projects")
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
                try:
                    ordered_path = mfile.get_ordered_path()
                    ordered_path = run_path_update(
                        mfile.mime_type,
                        mfile.metadata,
                        mfile.path,
                        ordered_path
                    )
                    sh.mkdir("-p",ordered_path)
                    ordered_path = os.path.join(
                        ordered_path,
                        u"{0}_{1}".format(os.path.basename(destination_path),
                                         os.path.basename(mfile.path.decode("utf8"))
                        )
                    )
                    log.info(u"File {0} @ {1}".format(str(mfile).decode("utf8"),ordered_path))
                    sh.ln("-s", destination_path, ordered_path)
                except sh.ErrorReturnCode_1:
                    pass
                except sh.ErrorReturnCode,e:
                    log.exception(e)
        except Exception, e:
            log.error("Organizer error {0}".format(mfile.path))
            log.exception(e)
        finally:
            for loaded_mfile in loaded_mfiles:
                try:
                    loaded_mfile.unload()
                except Exception, e:
                    log.error("Error unloading {0}".format(mfile.path))
                    log.exception(e)
            return True

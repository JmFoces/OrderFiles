
class UnknownFileSystemException(Exception):
    pass


class AlreadyMountedError(Exception):
    pass


class IncompatibleFS(Exception):
    pass

class UnableToHashFile(Exception):
    pass

class UnableToLoad(Exception):
    pass

class HadoopError(Exception):
    """Base class for Hadoop errors."""


class HdfsFileNotFoundError(HadoopError):
    """File or directory does not exist."""


class HdfsMakeDirError(HadoopError):
    """Error while creating directory."""


class HdfsNotADirectoryError(HadoopError):
    """Trying to use file as directory."""

class HdfsFileNotFoundError(FileNotFoundError):
    """File or directory does not exist."""


class HdfsMakeDirError(Exception):
    """Error while creating directory."""

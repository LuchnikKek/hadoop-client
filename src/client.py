from http import HTTPStatus

import requests
from pathlib import Path

from src.constants import LS_URI, MKDIR_URI
from src.exceptions import HdfsFileNotFoundError, HdfsMakeDirError, HdfsNotADirectoryError
from src.models import Document, FileType
from src.utils import concat_path


class HDFSClient:
    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user
        self.current_hadoop_dir = Path('/')
        self.current_local_dir = Path()

    def _hadoop_list_dir(self, abs_path: Path) -> list[dict]:
        """
        Return list of files in hadoop path.

        :raise HdfsFileNotFoundError: If path does not exist.
        :raise HdfsNotADirectoryError: If provided file, not a directory.
        """
        uri = LS_URI.format(host=self.host, port=self.port, path=abs_path)
        response = requests.get(url=uri)

        if not response.status_code == HTTPStatus.OK:
            raise HdfsFileNotFoundError('Directory %s does not exist' % abs_path)

        result = response.json().get('FileStatuses').get('FileStatus')

        if result and result[0]['type'] == FileType.FILE:
            raise HdfsNotADirectoryError('Provided %s is a file, not a directory' % abs_path)

        return result

    def ls(self, provided_path: str) -> list[Document]:
        """
        List directory.

        :param provided_path: A path to list with or without first '/' symbol.
        :return: A list of files and dirs. Add '/' symbol to each dir.
        """
        queried_directory = concat_path(self.current_hadoop_dir, provided_path)

        directory_data = self._hadoop_list_dir(queried_directory)
        documents = [Document.model_validate(file).filename for file in directory_data]
        return documents

    def mkdir(self, path: str, permission: str = '775') -> None:
        """
        Create directory.

        :param path: A string path to created directory.
        :param permission: A string with permission in octal. Default is '775'.
        """
        abs_path = str(concat_path(self.current_hadoop_dir, path))[1:]
        uri = MKDIR_URI.format(host=self.host, port=self.port, path=abs_path, permission=permission, owner=self.user)
        response = requests.put(url=uri, allow_redirects=False)

        if not response.status_code == HTTPStatus.OK:
            raise HdfsMakeDirError('Error while creating directory: %s' % response.json())

    def cd(self, provided_path: str) -> None:
        """
        Open directory.
        Use '..' to go one level upper.
        Absolute and relative paths are allowed.

        In fact, change pointer from current directory to provided
        """
        path = concat_path(self.current_hadoop_dir, provided_path)

        self._hadoop_list_dir(path)  # if path is not valid, raised Error

        self.current_hadoop_dir = path


if __name__ == '__main__':
    client = HDFSClient('localhost', 9870, 'custom_user')

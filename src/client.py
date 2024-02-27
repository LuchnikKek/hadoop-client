from http import HTTPStatus

import requests

from src.constants import LS_URI, MKDIR_URI
from src.exceptions import HdfsFileNotFoundError, HdfsMakeDirError
from src.models import Document


class HDFSClient:
    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user

    def ls(self, path: str):
        """
        List directory.

        :param path: A path to list with or without first '/' symbol.
        :return: A list of files and dirs. Add '/' symbol to each dir.
        """
        uri = LS_URI.format(host=self.host, port=self.port, path=path)
        response = requests.get(url=uri)

        if not response.status_code == HTTPStatus.OK:
            raise HdfsFileNotFoundError

        documents = [Document.model_validate(file) for file in response.json().get('FileStatuses').get('FileStatus')]
        return documents

    def mkdir(self, path: str, permission: str = '775') -> None:
        """
        Create directory.

        :param path: A string path to created directory.
        :param permission: A string with permission in octal. Default is '775'.
        """
        uri = MKDIR_URI.format(host=self.host, port=self.port, path=path, permission=permission, owner=self.user)
        response = requests.put(url=uri, allow_redirects=False)

        if not (resp_json := response.json().get('boolean')):
            raise HdfsMakeDirError(resp_json)


if __name__ == '__main__':
    client = HDFSClient('localhost', 9870, 'new_user')

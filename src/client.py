from http import HTTPStatus

import requests

from src.constants import LS_URI
from src.exceptions import HdfsFileNotFoundError
from src.models import Document


class HDFSClient:
    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user

    def ls(self, path: str):
        """List directory

        :param path: A path to list with or without first '/' symbol.
        :return: A list of files and dirs. Add '/' symbol to each dir.
        """
        uri = LS_URI.format(host=self.host, port=self.port, path=path)
        response = requests.get(url=uri)

        if not response.status_code == HTTPStatus.OK:
            raise HdfsFileNotFoundError

        documents = [Document.model_validate(file) for file in response.json().get('FileStatuses').get('FileStatus')]
        return [doc.filename for doc in documents]

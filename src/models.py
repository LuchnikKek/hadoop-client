from enum import Enum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class FileType(str, Enum):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"


class Document(BaseModel):
    access_time: int
    block_size: int
    children_num: int
    file_id: int
    group: str
    length: int
    modification_time: int
    owner: str
    path_suffix: str
    permission: str
    replication: int
    storage_policy: int
    type: FileType

    model_config = ConfigDict(alias_generator=to_camel)

    @property
    def filename(self):
        return self.path_suffix + '/' if self.type == FileType.DIRECTORY else self.path_suffix

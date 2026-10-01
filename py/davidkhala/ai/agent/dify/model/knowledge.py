from davidkhala.ai.agent.dify.const import IndexingStatus
from davidkhala.ai.agent.dify.model import ID


class Document(ID):
    position: int
    data_source_type: str
    data_source_info: dict[str, str|int|None]
    name: str
    indexing_status: IndexingStatus
    error: str | None
    enabled: bool


class Dataset(ID):
    name: str
    description: str

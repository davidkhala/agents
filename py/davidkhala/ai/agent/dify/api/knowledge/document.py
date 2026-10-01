
from typing import Iterable, Literal

import requests

from davidkhala.ai.agent.dify.api import API, Iterator
from davidkhala.ai.agent.dify.api.knowledge.dataset import Instance
from davidkhala.ai.agent.dify.api.knowledge.model import ChunkDict, DocumentModel, MetadataDocumentModel, \
    NonMetadataDocumentModel


class Document(API):
    def __init__(self, d: Instance, document_id: str):
        super().__init__(d.api_key, f"{d.base_url}/documents/{document_id}")

    def exist(self):
        try:
            self.get()
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False
            else:
                raise e

    def get(self,
            metadata: Literal['all', 'only', 'without'] = 'all'
            ) -> DocumentModel | MetadataDocumentModel | NonMetadataDocumentModel:
        """
        :param metadata:
            - 'only' returns metadata
            - 'without' returns anything without metadata
        """

        r = self.request(self.base_url, "GET", params={
            'metadata': metadata
        })
        match metadata:
            case 'only':
                return MetadataDocumentModel.model_validate(r)
            case 'without':
                return NonMetadataDocumentModel.model_validate(r)

        return DocumentModel.model_validate(r)

    def paginate_chunks(self, page=1, size=20, keyword=None):
        assert 0 < size < 101
        return self.request(f"{self.base_url}/segments", "GET", params={
            'page': page,
            'limit': size,
            'keyword': keyword
        })

    def list_chunks(self, keyword=None) -> Iterable[ChunkDict]:
        for chunk_batch in Iterator(self.paginate_chunks, keyword=keyword):
            for chunk in chunk_batch:
                yield chunk

    def delete(self):
        if self.exist():
            self.request(self.base_url, "DELETE")

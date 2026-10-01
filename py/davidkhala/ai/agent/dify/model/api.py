from abc import ABC
from datetime import datetime

from davidkhala.utils.http_request import Request

from davidkhala.ai.agent.dify.api.knowledge.model import MetadataType, DocMetadataModel


class DocumentMetadataProtocol(Request, ABC):
    base_url:str
    def list(self) -> list[DocMetadataModel]:
        r = self.request(f"{self.base_url}/metadata", "GET")
        return [DocMetadataModel.model_validate(_) for _ in r['doc_metadata']]

    def add(self, _type: MetadataType, name: str) -> str:
        r = self.request(f"{self.base_url}/metadata", "POST", json={
            'type': _type, 'name': name
        })
        return r['id']

    def rename(self, metadata_id: str, name: str) -> DocMetadataModel:
        r = self.request(f"{self.base_url}/metadata/{metadata_id}", "PATCH", json={
            'name': name,
            # type is immutable
        })
        return DocMetadataModel.model_validate(r)

    def delete(self, metadata_id: str):
        self.request(f"{self.base_url}/metadata/{metadata_id}", "DELETE")

    def set(self, *documents: str, metadata: dict):
        url = f"{self.base_url}/documents/metadata"
        metadata_list = []
        datasets = self.list()

        for name, value in metadata.items():
            _type: MetadataType
            match value:
                case str():
                    _type = "string"
                case datetime():
                    _type = "time"
                    value = int(value.timestamp())
                case _:
                    _type = "number"

            _id = next((_.id for _ in datasets if _.name == name), None)
            if not _id:
                _id = self.add(_type, name)

            metadata_list.append({
                'id': _id,
                'type': _type,
                'name': name, 'value': value
            })
        self.request(url, "POST", json={
            'operation_data': [
                {'document_id': document, 'metadata_list': metadata_list, "partial_update": False}
                for document in documents
            ],
        })

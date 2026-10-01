from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import requests

from davidkhala.ai.agent.dify.api import API, Iterator
from davidkhala.ai.agent.dify.api.knowledge.model import DatasetModel, NonMetadataDocumentModel
from davidkhala.ai.agent.dify.model.workflow import NodeProtocol


class Dataset(API):
    def __init__(self, api_key: str, base_url="https://api.dify.ai/v1"):
        super().__init__(api_key, f"{base_url}/datasets")

    def paginate_datasets(self, page=1, size=20, keyword=None):
        assert 0 < size < 101
        return self.request(self.base_url, "GET", params={
            'page': page,
            'limit': size,
            'keyword': keyword
        })

    def list_datasets(self, keyword=None) -> Iterable[DatasetModel]:
        for sub_list in Iterator(self.paginate_datasets, keyword=keyword):
            for dataset in sub_list:
                yield DatasetModel.model_validate(dataset)

    @property
    def ids(self):
        for dataset in self.list_datasets():
            yield dataset.id


class Instance(API):
    def __init__(self, d: Dataset, dataset_id: str):
        super().__init__(d.api_key, f"{d.base_url}/{dataset_id}")

    def get(self) -> DatasetModel:
        d = self.request(self.base_url, "GET")
        return DatasetModel.model_validate(d)

    def upload(self, filename, *, path=None, url=None, document_id=None):
        """
        don't work for .html
        work for .md
        """
        files = {}
        if path:
            with open(path, 'rb') as f:
                content = f.read()
            if not filename:
                filename = os.path.basename(path)
        elif url:
            r = requests.get(url)
            r.raise_for_status()
            if not filename:
                parsed_url = urlparse(url)
                filename = Path(parsed_url.path).name
            content = r.content
        files['file'] = (filename, content)
        if document_id:
            # don't work for html
            r = requests.post(f"{self.base_url}/documents/{document_id}/update-by-file", files=files,
                              **self.options)
        else:
            r = requests.post(f"{self.base_url}/document/create-by-file", files=files, **self.options)
        r = self.on_response(r)
        return r['document']

    def paginate_documents(self, page=1, size=20, keyword=None):
        assert 0 < size < 101
        return self.request(f"{self.base_url}/documents", "GET", params={
            'page': page,
            'limit': size,
            'keyword': keyword
        })

    def list_documents(self, keyword=None) -> Iterable[NonMetadataDocumentModel]:
        for document_batch in Iterator(self.paginate_documents, keyword=keyword):
            for document in document_batch:
                yield NonMetadataDocumentModel.model_validate(document)

    def has_document(self, name) -> bool:
        return any(name == item['name'] for row in self.list_documents() for item in row)

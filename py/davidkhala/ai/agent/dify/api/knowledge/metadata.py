from davidkhala.ai.agent.dify.api import API
from davidkhala.ai.agent.dify.api.knowledge.dataset import Dataset
from davidkhala.ai.agent.dify.api.knowledge.document import Document as DocumentAPI
from davidkhala.ai.agent.dify.api.knowledge.model import MetadataDocumentModel
from davidkhala.ai.agent.dify.model.api import DocumentMetadataProtocol


class Metadata(API, DocumentMetadataProtocol):

    def __init__(self, d: Dataset.Instance):
        super().__init__(d.api_key, d.base_url)
        self._ = d


    def of_document(self, document_id: str) -> MetadataDocumentModel:
        _ = DocumentAPI(self._, document_id)
        return _.get('only')

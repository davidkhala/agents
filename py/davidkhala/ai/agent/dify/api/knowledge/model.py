
from typing import List, Any, TypedDict, Literal

from pydantic import BaseModel

from davidkhala.ai.agent.dify.model import ID
from davidkhala.ai.agent.dify.model.knowledge import Document as DocumentBase


class RerankingModel(BaseModel):
    reranking_provider_name: str | None
    reranking_model_name: str | None


class KeywordSetting(BaseModel):
    keyword_weight: float


class VectorSetting(BaseModel):
    vector_weight: float
    embedding_model_name: str
    embedding_provider_name: str


class Weights(BaseModel):
    weight_type: str | None
    keyword_setting: KeywordSetting | None
    vector_setting: VectorSetting | None


class RetrievalModelDict(BaseModel):
    search_method: str
    reranking_enable: bool
    reranking_mode: str | None
    reranking_model: RerankingModel | None
    weights: Weights | None
    top_k: int | None
    score_threshold_enabled: bool
    score_threshold: float


class ExternalKnowledgeInfo(BaseModel):
    external_knowledge_id: str | None
    external_knowledge_api_id: str | None
    external_knowledge_api_name: str | None
    external_knowledge_api_endpoint: str | None


class ExternalRetrievalModel(BaseModel):
    top_k: int
    score_threshold: float
    score_threshold_enabled: bool


class IconInfo(BaseModel):
    icon_type: str | None
    icon: str | None
    icon_background: str | None
    icon_url: str | None


class DatasetModel(BaseModel):
    id: str
    name: str
    description: str | None = None
    provider: str
    permission: str
    data_source_type: str | None = None
    indexing_technique: str | None = None
    app_count: int
    document_count: int
    word_count: int
    created_by: str | None = None
    author_name: str | None = None
    created_at: int | None = None
    updated_by: str | None = None
    updated_at: int | None = None
    embedding_model: str | None = None
    embedding_model_provider: str | None = None
    embedding_available: bool
    retrieval_model_dict: RetrievalModelDict | None = None
    tags: List[Any] = []
    doc_form: str | None = None
    external_knowledge_info: ExternalKnowledgeInfo | None = None
    external_retrieval_model: ExternalRetrievalModel | None = None
    doc_metadata: List[Any] = []
    built_in_field_enabled: bool
    pipeline_id: str | None = None
    runtime_mode: Literal['rag_pipeline', 'standard']
    chunk_structure: str | None = None
    icon_info: IconInfo | None = None
    is_published: bool
    total_documents: int | None = None
    total_available_documents: int | None = None
    enable_api: bool
    is_multimodal: bool


class RulesModel(BaseModel):
    parent_mode: str


class DatasetProcessRuleModel(BaseModel):
    mode: str
    rules: RulesModel


MetadataType = Literal['string', 'number', 'time']

class DocMetadataModel(BaseModel):
    id: Literal['built-in'] | str
    name: str
    type: MetadataType
    value: Any | None = None # not used in definition
    count: int | None = None # used in definition


class DocumentProcessRuleModel(BaseModel):
    id: str
    dataset_id: str
    mode: str
    rules: RulesModel


class MetadataDocumentModel(ID):
    doc_type: str | None = None
    doc_metadata: list[DocMetadataModel]

    @property
    def custom_metadata(self) -> list[dict[str, Any]] | None:
        if not self.doc_metadata:
            return None
        return [{_.name: _.value} for _ in self.doc_metadata if _.id != 'built-in']


class NonMetadataDocumentModel(DocumentBase):
    dataset_process_rule_id: str
    dataset_process_rule: DatasetProcessRuleModel | None = None  # None for paginate_documents
    document_process_rule: DocumentProcessRuleModel | None = None  # None for paginate_documents
    created_from: str
    created_by: str
    created_at: int
    tokens: int | None
    completed_at: int | None = None  # None for paginate_documents
    updated_at: int | None = None  # None for paginate_documents
    indexing_latency: float | None = None  # None for paginate_documents
    disabled_at: int | None
    disabled_by: str | None
    archived: bool
    segment_count: int | None = None  # None for paginate_documents
    average_segment_length: int | None = None  # None for paginate_documents
    hit_count: int
    display_status: str
    doc_form: str
    doc_language: str | None = None  # None for paginate_documents
    summary_index_status: str | None
    need_summary: bool


class DocumentModel(NonMetadataDocumentModel, MetadataDocumentModel): ...


class ChunkDict(TypedDict):
    id: str
    position: int
    document_id: str
    content: str
    sign_content: str  # trimmed version of content
    answer: str | None  # only used in QA chunk
    word_count: int
    tokens: int
    keywords: list[str] | None
    index_node_id: str  # chunk 在向量索引中的节点 ID
    index_node_hash: str  # hash of sign_content
    hit_count: int
    enabled: bool
    status: str  # 'completed'
    created_at: int  # timestamp
    updated_at: int  # timestamp
    completed_at: int  # timestamp
    created_by: str  # user id
    child_chunks: list
    error: Any | None
    stopped_at: int | None  # timestamp
    disabled_at: int | None  # timestamp

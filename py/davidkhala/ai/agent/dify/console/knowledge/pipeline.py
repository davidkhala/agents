from typing import Any

from davidkhala.utils.http_request.stream import Request as StreamRequest, as_sse
from pydantic import BaseModel, Field

from davidkhala.ai.agent.dify.console.session import ConsoleDerived
from davidkhala.ai.agent.dify.model import User
from davidkhala.ai.agent.dify.model.knowledge import Dataset, Document
from davidkhala.ai.agent.dify.model.workflow import NodeProtocol, Graph


class RAGPipelineVariable(BaseModel):
    label: str
    variable: str
    type: str
    belong_to_node_id: str
    max_length: int | None = None
    required: bool = False
    unit: str | None = None
    default_value: Any | None = None
    options: list[Any] = Field(default_factory=list)
    placeholder: str | None = None
    tooltips: str | None = None
    allowed_file_types: str | None = None
    allow_file_extension: str | None = None
    allow_file_upload_methods: str | None = None


class PipelineModel(BaseModel):
    id: str
    graph: Graph
    features: dict[str, Any] = Field(default_factory=dict)
    hash: str
    version: str
    marked_name: str = ""
    marked_comment: str = ""
    created_by: User
    created_at: int
    updated_by: User | None = None
    updated_at: int
    tool_published: bool = False
    environment_variables: list[dict[str, Any]]
    conversation_variables: list[dict[str, Any]]
    rag_pipeline_variables: list[RAGPipelineVariable]


class DatasetResult(Dataset):
    chunk_structure: str


class RunResult(BaseModel):
    batch: str
    dataset: DatasetResult
    documents: list[Document]


from davidkhala.ai.agent.dify.api.knowledge.dataset import Instance


class Pipeline(ConsoleDerived):

    def async_run(self, pipeline: str, node: NodeProtocol, inputs: dict, datasource_info_list: list[dict]) -> RunResult:
        """Ingest new document"""
        url = f"{self.base_url}/rag/pipelines/{pipeline}/workflows/published/run"
        r = self.request(url, "POST", json={
            'inputs': inputs,
            'start_node_id': node.id,
            'is_preview': False,
            'response_mode': "blocking",
            "datasource_info_list": datasource_info_list,
            'datasource_type': node.datasource_type
        })
        return RunResult.model_validate(r)

    def get(self, pipeline: str):
        url = f"{self.base_url}/rag/pipelines/{pipeline}/workflows/publish"
        r = self.request(url, "GET")
        return PipelineModel.model_validate(r)

    def filecrawl(self,
                  url: str, dataset_instance: Instance, firecrawl_key_name: str,
                  *, pages=1):

        from davidkhala.ai.agent.dify.console.knowledge.dataset import DocumentOperation
        from davidkhala.ai.agent.dify.console.plugin import ConsoleTool

        p_id = dataset_instance.get().pipeline_id

        kb_console = Datasource(self.user)

        console_tool = ConsoleTool(self.user)

        credential_id = console_tool.credential_id_by(firecrawl_key_name, 'langgenius', "firecrawl")
        assert credential_id is not None
        pipeline = self.get(p_id)
        nodes = pipeline.graph.datasources
        node = next((n for n in nodes if n.data.title == 'Firecrawl'), None)

        datasource_info_list = []

        if pages > 1:
            sources_r = kb_console.run_firecrawl(p_id, node, inputs={
                "url": url,
                "subpage": False,
                "pages": pages
            }, credential_id=credential_id)

            datasource_info_list = []
            from davidkhala.ai.agent.dify.plugins.firecrawl import Console as FirecrawlModel
            for source in sources_r:
                source['credential_id'] = credential_id
                source['title'] = source['source_url']
                FirecrawlModel.model_validate(source)  # schema validation
                datasource_info_list.append(source)
            assert len(datasource_info_list) == pages
        elif pages == 1:
            f = {
                'title': url,
                'credential_id': credential_id,
                'source_url': url
            }
            datasource_info_list.append(f)
        else:
            raise Exception(f"invalid pages == {pages}")
        run_r = self.async_run(p_id, node, inputs={
        }, datasource_info_list=datasource_info_list)
        # wait until
        assert len(run_r.documents) == pages

        console_ops = DocumentOperation(self.user, run_r.dataset.id)
        returns = []
        from davidkhala.ai.agent.dify.const import IndexingStatus
        for document in run_r.documents:
            final = console_ops.wait_until(document.id,
                                           from_status=[IndexingStatus.WAITING, IndexingStatus.PARSING,
                                                        IndexingStatus.COMPLETED, IndexingStatus.FAILED])
            returns.append(final)
        return returns


class Datasource(ConsoleDerived):
    class FirecrawlOutput(BaseModel):
        source_url: str
        description: str
        title: str
        credential_id: str
        content: str

    def run_firecrawl(self, pipeline: str, node: NodeProtocol,
                      *,
                      inputs: dict,
                      credential_id: str
                      ):

        url = f"{self.base_url}/rag/pipelines/{pipeline}/workflows/published/datasource/nodes/{node.id}/run"

        stream_request = StreamRequest(self)
        response = stream_request.request(url, 'POST', json={
            'inputs': inputs,
            'datasource_type': node.datasource_type,
            'credential_id': credential_id,
            "response_mode": "streaming"  # blocking is not available
        })

        for data in as_sse(response):
            event = data['event']
            match event:
                case 'datasource_completed':
                    return data['data']
                case 'datasource_processing':
                    print(data)
                case 'datasource_error':
                    raise Exception(data['error'])

        return None

    def upload(self):
        "http://localhost/console/api/files/upload?source=datasets"
        # TODO
        "form data"
        {
            "file": "body"
        }
        r = {
            "id": "3898db5b-eb72-4f11-b507-628ad5d28887",
            "name": "Professional Diploma Meister Power Electrical Engineering - Technological and Higher Education Institute of Hong Kong.html",
            "size": 254362,
            "extension": "html",
            "mime_type": "text\/html",
            "created_by": "dbd0b38b-5ef1-4123-8c3f-0c82eb1feacd",
            "created_at": 1764943811,
            "source_url": "\/files\/3898db5b-eb72-4f11-b507-628ad5d28887\/file-preview?timestamp=1764943811&nonce=43b0ff5a13372415be79de4cc7ef398c&sign=7OJ2wiVYc4tygl7yvM1sPn7s0WXDlhHxgX76bsGTD94%3D"
        }

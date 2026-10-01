from enum import Enum
from typing import Protocol, Literal, Any, Optional

from pydantic import BaseModel, Field




class NodeProtocol(Protocol):
    id:str
    datasource_type: str


class Position(BaseModel):
    x: float
    y: float
class Viewport(Position):
    zoom: float

class JsonData(BaseModel):
    data: list


class NodeOutput(BaseModel):
    """Schema for Output of a Dify node"""
    text: str
    files: list
    json_: list[JsonData] = Field(alias="json") # avoid conflict with .json()




class NodeData(BaseModel):
    class Type(str, Enum):
        SOURCE = 'datasource'
        CHUNKER = 'knowledge-index'
        TOOL = 'tool'

    type: Type | str  # not limit to built-in types
    title: str | None = None
    selected: bool

    # datasource
    datasource_parameters: dict[str, Any] | None = None
    datasource_configurations: dict[str, Any] | None = None
    plugin_id: str | None = None
    provider_type: str | None = None
    provider_name: str | None = None
    datasource_name: str | None = None
    datasource_label: str | None = None
    plugin_unique_identifier: str | None = None

    # tool
    tool_parameters: dict[str, Any] | None = None
    tool_configurations: dict[str, Any] | None = None
    tool_node_version: str | None = None
    provider_id: str | None = None
    provider_icon: str | None = None
    tool_name: str | None = None
    tool_label: str | None = None
    tool_description: str | None = None
    is_team_authorization: bool | None = None
    paramSchemas: list[Any] | None = None
    params: dict[str, Any] | None = None

    # knowledge index
    index_chunk_variable_selector: list[str] | None = None
    keyword_number: int | None = None
    retrieval_model: dict[str, Any] | None = None
    chunk_structure: str | None = None
    indexing_technique: str | None = None
    embedding_model: str | None = None
    embedding_model_provider: str | None = None

class Node(BaseModel):
    @property
    def datasource_type(self): return self.data.provider_type
    id: str
    type: Literal['custom']
    data: NodeData
    position: Position
    targetPosition: str | None = None
    sourcePosition: str | None = None
    positionAbsolute: Position | None = None
    width: float | None = None
    height: float | None = None
    selected: bool | None = False

class EdgeData(BaseModel):
    sourceType: str | None = None
    targetType: str | None = None
    isInIteration: bool | None = False
    isInLoop: bool | None = False
class Edge(BaseModel):
    id: str
    type: str
    source: str
    target: str
    sourceHandle: str | None = None
    targetHandle: str | None = None
    data: EdgeData | None = None
    zIndex: int | None = None


class Graph(BaseModel):
    nodes: list[Node]
    edges: list[Edge]
    viewport: Viewport

    @property
    def datasources(self):
        return [node for node in self.nodes if node.data.type == NodeData.Type.SOURCE]


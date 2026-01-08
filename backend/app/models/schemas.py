"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str = Field(..., min_length=1, max_length=1000)
    index_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)


class Entity(BaseModel):
    """Model for extracted entities."""
    name: str
    type: str
    source_chunk_id: Optional[int] = None


class Relationship(BaseModel):
    """Model for entity relationships."""
    from_entity: str
    to_entity: str
    relation: str


class GraphNode(BaseModel):
    """Model for graph nodes."""
    id: str
    label: str


class GraphEdge(BaseModel):
    """Model for graph edges."""
    source: str
    target: str
    label: str


class GraphData(BaseModel):
    """Model for graph visualization data."""
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    answer: str
    entities: List[Entity]
    relationships: List[Relationship]
    graph_data: GraphData
    snippets: List[str]
    status: str = "success"


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    status: str
    message: str
    index_id: str
    chunks_count: int


class StatusResponse(BaseModel):
    """Response model for status endpoint."""
    status: str
    message: str
    version: str = "1.0.0"

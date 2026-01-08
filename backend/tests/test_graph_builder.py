"""
Unit tests for graph builder module.
"""
import pytest
from app.modules.graph_builder import KnowledgeGraphBuilder


class TestKnowledgeGraphBuilder:
    @pytest.fixture
    def builder(self):
        return KnowledgeGraphBuilder()
    
    def test_build_graph_basic(self, builder):
        entities = [
            {'name': 'Alice', 'type': 'PERSON', 'source_chunk_id': 0},
            {'name': 'Bob', 'type': 'PERSON', 'source_chunk_id': 0},
        ]
        entity_chunk_map = {
            0: [
                {'name': 'Alice', 'type': 'PERSON'},
                {'name': 'Bob', 'type': 'PERSON'}
            ]
        }
        chunks = ["Alice and Bob are friends."]
        
        graph = builder.build_graph(entities, entity_chunk_map, chunks)
        
        assert graph.number_of_nodes() >= 2
        assert 'Alice' in graph.nodes()
        assert 'Bob' in graph.nodes()
    
    def test_get_graph_data(self, builder):
        entities = [
            {'name': 'Apple', 'type': 'ORG', 'source_chunk_id': 0},
            {'name': 'Microsoft', 'type': 'ORG', 'source_chunk_id': 0},
        ]
        entity_chunk_map = {
            0: [
                {'name': 'Apple', 'type': 'ORG'},
                {'name': 'Microsoft', 'type': 'ORG'}
            ]
        }
        chunks = ["Apple and Microsoft are tech companies."]
        
        builder.build_graph(entities, entity_chunk_map, chunks)
        graph_data = builder.get_graph_data()
        
        assert 'nodes' in graph_data
        assert 'edges' in graph_data
        assert len(graph_data['nodes']) > 0
    
    def test_get_relationships(self, builder):
        entities = [
            {'name': 'Google', 'type': 'ORG', 'source_chunk_id': 0},
            {'name': 'YouTube', 'type': 'PRODUCT', 'source_chunk_id': 0},
        ]
        entity_chunk_map = {
            0: [
                {'name': 'Google', 'type': 'ORG'},
                {'name': 'YouTube', 'type': 'PRODUCT'}
            ]
        }
        chunks = ["Google owns YouTube."]
        
        builder.build_graph(entities, entity_chunk_map, chunks)
        relationships = builder.get_relationships()
        
        assert isinstance(relationships, list)

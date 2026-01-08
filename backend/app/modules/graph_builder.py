"""
Knowledge graph construction module using NetworkX.
"""
from typing import List, Dict, Tuple, Set
import networkx as nx
from collections import defaultdict

# Optional spaCy import - may fail on Python 3.14+
try:
    import spacy
    SPACY_AVAILABLE = True
except Exception as e:
    print(f"Warning: spaCy not available ({e}). Graph builder will work with basic features.")
    SPACY_AVAILABLE = False


class KnowledgeGraphBuilder:
    """Build knowledge graphs from extracted entities."""
    
    def __init__(self):
        """Initialize knowledge graph builder."""
        self.graph = nx.Graph()
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except Exception:
                pass
    
    def build_graph(
        self,
        entities: List[Dict[str, str]],
        entity_chunk_map: Dict,
        chunks: List[str]
    ) -> nx.Graph:
        """
        Build knowledge graph from entities.
        
        Args:
            entities: List of extracted entities
            entity_chunk_map: Mapping of chunk indices to entities
            chunks: Original text chunks
            
        Returns:
            NetworkX graph
        """
        self.graph = nx.Graph()
        
        # Add entity nodes
        for entity in entities:
            self.graph.add_node(
                entity['name'],
                type=entity['type'],
                source_chunk=entity.get('source_chunk_id', 0)
            )
        
        # Add edges for co-occurrence
        self._add_cooccurrence_edges(entity_chunk_map, chunks, entities)
        
        # Add edges for dependencies (if spaCy available)
        if self.nlp:
            self._add_dependency_edges(chunks, entities)
        
        return self.graph
    
    def _add_cooccurrence_edges(
        self,
        entity_chunk_map: Dict,
        chunks: List[str],
        entities: List[Dict]
    ):
        """Add edges for entities that co-occur in same chunk."""
        entity_names = {ent['name'] for ent in entities}
        
        for chunk_idx, chunk_entities in entity_chunk_map.items():
            # Get entity names in this chunk
            names_in_chunk = [ent['name'] for ent in chunk_entities if ent['name'] in entity_names]
            
            # Create edges between all pairs
            for i, name1 in enumerate(names_in_chunk):
                for name2 in names_in_chunk[i+1:]:
                    if name1 != name2:
                        self.graph.add_edge(
                            name1,
                            name2,
                            relation='co-occurs-in-chunk',
                            weight=1.0
                        )
    
    def _add_dependency_edges(self, chunks: List[str], entities: List[Dict]):
        """Add edges based on syntactic dependencies."""
        if not self.nlp:
            return
        
        entity_names = {ent['name'].lower() for ent in entities}
        
        for chunk in chunks:
            doc = self.nlp(chunk)
            
            # Find verb dependencies between entities
            for token in doc:
                if token.pos_ == 'VERB':
                    # Find subject and object
                    subj = None
                    obj = None
                    
                    for child in token.children:
                        if child.dep_ == 'nsubj' and any(
                            child.text.lower() in en for en in entity_names
                        ):
                            subj = child.text
                        elif child.dep_ == 'dobj' and any(
                            child.text.lower() in en for en in entity_names
                        ):
                            obj = child.text
                    
                    # Add edge with verb as relation
                    if subj and obj and subj in self.graph and obj in self.graph:
                        self.graph.add_edge(
                            subj,
                            obj,
                            relation=token.lemma_,
                            weight=2.0
                        )
    
    def get_graph_data(self) -> Dict:
        """
        Convert NetworkX graph to JSON-serializable format for visualization.
        
        Returns:
            Dict with nodes and edges for Cytoscape
        """
        nodes = []
        edges = []
        
        # Add nodes
        for node in self.graph.nodes():
            node_data = self.graph.nodes[node]
            nodes.append({
                'id': str(node),
                'label': str(node),
                'type': node_data.get('type', 'UNKNOWN')
            })
        
        # Add edges
        seen_edges = set()
        for source, target, data in self.graph.edges(data=True):
            edge_key = tuple(sorted([source, target]))
            if edge_key not in seen_edges:
                edges.append({
                    'source': str(source),
                    'target': str(target),
                    'label': data.get('relation', 'related-to')
                })
                seen_edges.add(edge_key)
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def get_relationships(self) -> List[Dict[str, str]]:
        """
        Get relationships from graph.
        
        Returns:
            List of relationship dicts
        """
        relationships = []
        seen = set()
        
        for source, target, data in self.graph.edges(data=True):
            rel_key = tuple(sorted([source, target]))
            if rel_key not in seen:
                relationships.append({
                    'from_entity': str(source),
                    'to_entity': str(target),
                    'relation': data.get('relation', 'related-to')
                })
                seen.add(rel_key)
        
        return relationships

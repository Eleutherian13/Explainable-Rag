"""
Unit tests for entity extraction module.
"""
import pytest
from app.modules.entity_extraction import EntityExtractor


class TestEntityExtractor:
    @pytest.fixture
    def extractor(self):
        return EntityExtractor('en_core_web_sm')
    
    def test_extract_entities_basic(self, extractor):
        text = "John works at OpenAI in San Francisco."
        entities = extractor.extract_entities(text)
        
        assert len(entities) > 0
        entity_texts = [e['name'] for e in entities]
        assert 'John' in entity_texts
        assert 'OpenAI' in entity_texts
    
    def test_extract_entities_empty(self, extractor):
        text = "This is just some random text."
        entities = extractor.extract_entities(text)
        # May or may not have entities, just ensure it runs
        assert isinstance(entities, list)
    
    def test_extract_from_chunks(self, extractor):
        chunks = [
            "Apple is a tech company founded by Steve Jobs.",
            "Microsoft competes with Apple in the tech industry."
        ]
        entities, entity_map = extractor.extract_from_chunks(chunks)
        
        assert isinstance(entities, list)
        assert isinstance(entity_map, dict)
        assert len(entity_map) == 2
    
    def test_extract_noun_phrases(self, extractor):
        text = "Machine learning is a subset of artificial intelligence."
        phrases = extractor.extract_noun_phrases(text)
        
        assert len(phrases) > 0
        assert isinstance(phrases, list)

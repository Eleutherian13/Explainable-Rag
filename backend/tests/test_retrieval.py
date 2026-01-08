"""
Unit tests for retrieval module.
"""
import pytest
import numpy as np
from app.modules.retrieval import EmbeddingModel, FAISSRetriever


class TestEmbeddingModel:
    @pytest.fixture
    def embedding_model(self):
        return EmbeddingModel('all-MiniLM-L6-v2')
    
    def test_embedding_dimension(self, embedding_model):
        assert embedding_model.dimension == 384
    
    def test_encode_single(self, embedding_model):
        texts = ["Hello world"]
        embeddings = embedding_model.encode(texts)
        assert embeddings.shape == (1, 384)
        assert embeddings.dtype == np.float32
    
    def test_encode_multiple(self, embedding_model):
        texts = ["Hello", "World", "Test"]
        embeddings = embedding_model.encode(texts)
        assert embeddings.shape == (3, 384)


class TestFAISSRetriever:
    @pytest.fixture
    def retriever(self):
        embedding_model = EmbeddingModel('all-MiniLM-L6-v2')
        return FAISSRetriever(embedding_model)
    
    def test_build_index(self, retriever):
        texts = ["This is a test", "Another document", "Third chunk"]
        sources = ["doc1.txt", "doc1.txt", "doc2.txt"]
        
        retriever.build_index(texts, sources)
        assert retriever.is_indexed()
        assert len(retriever.chunks) == 3
    
    def test_retrieve(self, retriever):
        texts = ["machine learning", "deep learning", "artificial intelligence"]
        sources = ["doc.txt"] * 3
        
        retriever.build_index(texts, sources)
        chunks, srcs, sims = retriever.retrieve("machine learning", k=2)
        
        assert len(chunks) == 2
        assert len(srcs) == 2
        assert len(sims) == 2
        assert sims[0] > sims[1]  # Most relevant first
    
    def test_retrieve_without_index(self, retriever):
        chunks, srcs, sims = retriever.retrieve("test", k=5)
        assert len(chunks) == 0

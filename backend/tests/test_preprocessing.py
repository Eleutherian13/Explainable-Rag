"""
Unit tests for preprocessing module.
"""
import pytest
from app.modules.preprocessing import (
    clean_text, chunk_text, extract_text_from_file
)


class TestTextCleaning:
    def test_clean_text_removes_extra_whitespace(self):
        text = "This   is   a   test"
        result = clean_text(text)
        assert result == "This is a test"
    
    def test_clean_text_removes_special_chars(self):
        text = "Hello@World#Test$123"
        result = clean_text(text)
        # Should keep alphanumeric and basic punctuation
        assert "@" not in result
        assert "#" not in result


class TestChunking:
    def test_chunk_text_basic(self):
        text = "Sentence one. Sentence two. Sentence three. Sentence four."
        chunks = chunk_text(text, chunk_size=10, overlap=2)
        assert len(chunks) > 0
        assert all(isinstance(c, str) for c in chunks)
    
    def test_chunk_text_empty(self):
        text = ""
        chunks = chunk_text(text)
        assert len(chunks) == 0
    
    def test_chunks_not_empty(self):
        text = "This is a test. " * 20
        chunks = chunk_text(text)
        assert all(len(c) > 0 for c in chunks)


class TestFileExtraction:
    def test_extract_text_from_txt(self):
        content = b"This is test content"
        result = extract_text_from_file(content, "test.txt")
        assert "This is test content" in result
    
    def test_unsupported_format(self):
        content = b"test"
        result = extract_text_from_file(content, "test.xyz")
        assert result == ""

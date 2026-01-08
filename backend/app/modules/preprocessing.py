"""
Document preprocessing and chunking module.
"""
import re
from typing import List, Tuple
import pdfplumber
import pypdf
from pathlib import Path
import tempfile
import os


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extract text from uploaded file (PDF or text).
    
    Args:
        file_content: File content as bytes
        filename: Filename to determine type
        
    Returns:
        Extracted text
    """
    if filename.lower().endswith('.pdf'):
        # Save to temp file and read - use proper temp directory for cross-platform compatibility
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_path = temp_file.name
            temp_file.write(file_content)
        
        try:
            text = extract_text_from_pdf(temp_path)
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except Exception:
                pass
        return text
    elif filename.lower().endswith(('.txt', '.md')):
        return file_content.decode('utf-8', errors='ignore')
    else:
        return ""


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\']', '', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Approximate words per chunk
        overlap: Words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        words = sentence.split()
        sentence_size = len(words)
        
        if current_size + sentence_size <= chunk_size:
            current_chunk.append(sentence)
            current_size += sentence_size
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                # Keep overlap
                current_chunk = current_chunk[-(overlap // 10):] if overlap else []
                current_size = sum(len(s.split()) for s in current_chunk)
            current_chunk.append(sentence)
            current_size += sentence_size
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return [c.strip() for c in chunks if c.strip()]


def preprocess_documents(file_contents: List[Tuple[bytes, str]]) -> Tuple[List[str], List[str]]:
    """
    Preprocess multiple uploaded documents.
    
    Args:
        file_contents: List of (content, filename) tuples
        
    Returns:
        Tuple of (chunks, sources)
    """
    all_chunks = []
    all_sources = []
    
    for content, filename in file_contents:
        # Extract text
        text = extract_text_from_file(content, filename)
        # Clean text
        text = clean_text(text)
        # Split into chunks
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
        all_sources.extend([filename] * len(chunks))
    
    return all_chunks, all_sources

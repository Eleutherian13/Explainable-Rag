"""
API Client Examples for Explainable RAG System

This file demonstrates how to interact with the API using Python.
"""

import requests
import json
from pathlib import Path
from typing import Dict, List

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30


class RAGClient:
    """Client for interacting with Explainable RAG API."""
    
    def __init__(self, base_url: str = BASE_URL):
        """Initialize the client."""
        self.base_url = base_url
        self.session_id = None
    
    def check_health(self) -> bool:
        """Check if API is healthy."""
        try:
            response = requests.get(
                f"{self.base_url}/status",
                timeout=TIMEOUT
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def upload_documents(self, file_paths: List[str]) -> Dict:
        """
        Upload documents to the API.
        
        Args:
            file_paths: List of paths to PDF/TXT/MD files
            
        Returns:
            Response with session ID and metadata
        """
        files = []
        for path in file_paths:
            if Path(path).exists():
                files.append(('files', open(path, 'rb')))
            else:
                print(f"Warning: File not found: {path}")
        
        if not files:
            raise ValueError("No valid files provided")
        
        try:
            response = requests.post(
                f"{self.base_url}/upload",
                files=files,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            self.session_id = data['index_id']
            print(f"✓ Documents uploaded successfully")
            print(f"  Session ID: {self.session_id}")
            print(f"  Chunks: {data['chunks_count']}")
            
            return data
            
        finally:
            # Close file handles
            for _, file_obj in files:
                file_obj.close()
    
    def query(self, query_text: str, top_k: int = 5) -> Dict:
        """
        Submit a query to the system.
        
        Args:
            query_text: Natural language query
            top_k: Number of chunks to retrieve (default: 5)
            
        Returns:
            Response with answer, entities, graph, and snippets
        """
        if not self.session_id:
            raise ValueError("No session ID. Upload documents first.")
        
        payload = {
            "query": query_text,
            "index_id": self.session_id,
            "top_k": top_k
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/query",
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            print(f"\n✓ Query processed successfully")
            print(f"\nAnswer: {data['answer']}")
            print(f"\nEntities found: {len(data['entities'])}")
            print(f"Relationships: {len(data['relationships'])}")
            print(f"Source snippets: {len(data['snippets'])}")
            
            return data
            
        except requests.exceptions.Timeout:
            print("Query timed out. The system may be processing a large corpus.")
            raise
    
    def clear_session(self, session_id: str = None) -> Dict:
        """Clear a session."""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.post(
            f"{self.base_url}/clear",
            params={"index_id": sid},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        if sid == self.session_id:
            self.session_id = None
        
        print(f"✓ Session cleared: {sid}")
        return response.json()
    
    def print_results(self, results: Dict) -> None:
        """Pretty print query results."""
        print("\n" + "="*60)
        print("QUERY RESULTS")
        print("="*60)
        
        # Answer
        print("\n[ANSWER]")
        print(results['answer'])
        
        # Entities
        if results['entities']:
            print("\n[ENTITIES]")
            for entity in results['entities']:
                print(f"  • {entity['name']} ({entity['type']})")
        
        # Relationships
        if results['relationships']:
            print("\n[RELATIONSHIPS]")
            for rel in results['relationships']:
                print(f"  • {rel['from_entity']} --[{rel['relation']}]--> {rel['to_entity']}")
        
        # Source Snippets
        if results['snippets']:
            print("\n[SOURCE SNIPPETS]")
            for i, snippet in enumerate(results['snippets'], 1):
                print(f"\n  Snippet {i}:")
                print(f"  {snippet[:200]}...")
        
        # Graph
        if results['graph_data']:
            graph = results['graph_data']
            print(f"\n[KNOWLEDGE GRAPH]")
            print(f"  Nodes: {len(graph['nodes'])}")
            print(f"  Edges: {len(graph['edges'])}")
        
        print("\n" + "="*60)


# Example Usage

if __name__ == "__main__":
    # Initialize client
    client = RAGClient()
    
    # Check if API is running
    if not client.check_health():
        print("❌ API is not accessible at", BASE_URL)
        print("Make sure the backend is running: docker-compose up")
        exit(1)
    
    print("✓ API is healthy")
    
    # Example 1: Upload documents
    print("\n--- Example 1: Upload Documents ---")
    try:
        # Create sample file for demo
        sample_file = "sample_document.txt"
        with open(sample_file, 'w') as f:
            f.write("""
            Artificial Intelligence (AI) is intelligence demonstrated by machines.
            Machine Learning is a method of data analysis that automates analytical model building.
            Deep Learning is part of machine learning methods based on artificial neural networks.
            
            OpenAI is an AI research lab. It created GPT-4, a large language model.
            Google DeepMind develops AI systems. It created AlphaGo, which plays the game Go.
            """)
        
        result = client.upload_documents([sample_file])
        print(f"Upload result: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
    
    # Example 2: Submit a query
    print("\n--- Example 2: Submit Query ---")
    try:
        query_text = "What is machine learning?"
        results = client.query(query_text)
        client.print_results(results)
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
    
    # Example 3: Another query
    print("\n--- Example 3: Another Query ---")
    try:
        query_text = "Who created GPT-4?"
        results = client.query(query_text)
        client.print_results(results)
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
    
    # Cleanup
    print("\n--- Cleanup ---")
    try:
        client.clear_session()
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
    
    # Clean up sample file
    Path(sample_file).unlink(missing_ok=True)
    
    print("\n✓ Example completed!")

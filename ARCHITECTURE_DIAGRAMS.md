# System Architecture Diagram

## Visual System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                            USER'S WEB BROWSER                             │
│                          (Any modern browser)                             │
│                                                                             │
└────────────────────────────────┬──────────────────────────────────────────┘
                                 │
                    HTTP (REST API, JSON)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                     FRONTEND (React + Vite)                              │
│                      Port 3000 (Docker)                                  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                        Dashboard (Main Layout)                     │   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐  ┌──────────────────────┐              │   │
│  │  │ DocumentUpload       │  │ QueryForm            │              │   │
│  │  │ - Drag & drop        │  │ - Input field        │              │   │
│  │  │ - File validation    │  │ - Submit button      │              │   │
│  │  └──────────────────────┘  └──────────────────────┘              │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │                    Results Panel                           │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │   │
│  │  │  │ Answer Tab   │  │ Graph Tab    │  │ Entities Tab │  │   │   │
│  │  │  │ - AI response│  │ - Cytoscape  │  │ - List table │  │   │   │
│  │  │  │ - Markdown   │  │ - Interactive│  │ - Type badges│  │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │   │
│  │  │                                                           │   │   │
│  │  │  Source Snippets View                                    │   │   │
│  │  │  - Retrieved text chunks                                │   │   │
│  │  │  - Context for answers                                  │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  State Management: Zustand Store                                         │
│  - indexId, query, results, loading, error                             │
│                                                                             │
│  API Service: Axios HTTP Client                                         │
│  - uploadDocuments(), submitQuery(), getStatus()                        │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                         HTTP/REST (JSON payloads)
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                   BACKEND (FastAPI) - Port 8000                          │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                      FastAPI Application                            │  │
│  │                                                                      │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │  │
│  │  │ POST /upload   │  │ POST /query    │  │ GET /status    │       │  │
│  │  │ - File input   │  │ - Query string │  │ - Health check │       │  │
│  │  │ - Multipart    │  │ - Session ID   │  │                │       │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘       │  │
│  │                                                                      │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                      │                                    │
│                    ┌───────────────────────────────┐                     │
│                    │    RAG Processing Pipeline     │                     │
│                    └───────────────────────────────┘                     │
│                                      │                                    │
│          ┌──────────────┬──────────────┬──────────────┐                 │
│          ▼              ▼              ▼              ▼                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │Preprocessing │ │  Retrieval   │ │  Extraction  │ │Graph Builder │ │
│  │              │ │              │ │              │ │              │ │
│  │ - Extract    │ │ - Embedding  │ │ - NER        │ │ - Entities   │ │
│  │   text       │ │ - FAISS      │ │ - Types      │ │ - Edges      │ │
│  │ - Clean      │ │ - Search     │ │ - Normalize  │ │ - Serialize  │ │
│  │ - Chunk      │ │ - Top-k      │ │              │ │              │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ │
│          │              │              │              │               │
│          └──────────────┼──────────────┼──────────────┘               │
│                         │              │                              │
│          ┌──────────────┴──────────────┘                             │
│          │                                                             │
│          ▼                                                             │
│  ┌──────────────────────────────┐                                    │
│  │   Answer Generator (LLM)     │                                    │
│  │                              │                                    │
│  │ - OpenAI API (primary)       │                                    │
│  │ - Fallback heuristic         │                                    │
│  │ - Prompt engineering         │                                    │
│  └──────────────────────────────┘                                    │
│                  │                                                    │
│                  ▼                                                    │
│  ┌──────────────────────────────┐                                    │
│  │  Response Compilation        │                                    │
│  │                              │                                    │
│  │ - Answer                     │                                    │
│  │ - Entities                   │                                    │
│  │ - Relationships              │                                    │
│  │ - Graph (Cytoscape format)  │                                    │
│  │ - Source snippets            │                                    │
│  └──────────────────────────────┘                                    │
│                                                                        │
└─────────────────────────────────────┬────────────────────────────────┘
                                      │
                         JSON Response (REST)
                                      │
                                      ▼
                            Frontend receives JSON
                            Renders results to user
```

## Data Flow for Upload Operation

```
Step 1: User Uploads Files
────────────────────────────
     User selects files
            ↓
    File input element
            ↓
    Multi-part form data
            ↓
  POST /upload endpoint


Step 2: Backend Processing (Preprocessing Module)
──────────────────────────────────────────────────
    File bytes received
            ↓
    Detect file type
            ↓
    Extract text (PyMuPDF/TextExtractor)
            ↓
    Clean text (remove special chars, normalize)
            ↓
    Split into chunks (300 words, 50 word overlap)
            ↓
    Create metadata (source file, chunk index)


Step 3: Embedding & Indexing (Retrieval Module)
────────────────────────────────────────────────
    Text chunks
            ↓
    SentenceTransformers encoder
            ↓
    384-dim embeddings
            ↓
    FAISS Index creation
    (FlatL2 - Euclidean distance)
            ↓
    Store in session


Step 4: Entity Extraction (Entity Extraction Module)
──────────────────────────────────────────────────────
    For each chunk:
            ↓
    spaCy NER pipeline
            ↓
    Extract (name, type, position)
            ↓
    Deduplicate entities
            ↓
    Create entity → chunk mapping


Step 5: Graph Construction (Graph Builder Module)
──────────────────────────────────────────────────
    Get all unique entities
            ↓
    Add as NetworkX nodes
            ↓
    Find co-occurring entities
            ↓
    Add edges with "co-occurs" relation
            ↓
    Optional: Parse dependencies for verb-based edges


Step 6: Response
────────────────
    JSON response:
    {
        "status": "success",
        "index_id": "uuid",
        "chunks_count": 123,
        "message": "..."
    }
            ↓
    Frontend stores index_id
            ↓
    User can now query
```

## Data Flow for Query Operation

```
Step 1: User Submits Query
───────────────────────────
    User types question
            ↓
    Clicks "Submit Query"
            ↓
    POST /query {query, index_id}


Step 2: Embedding & Search (Retrieval Module)
──────────────────────────────────────────────
    Query text
            ↓
    SentenceTransformers encoder
            ↓
    Query embedding (384-dim)
            ↓
    FAISS search (Euclidean distance)
            ↓
    Get top-5 similar chunks
            ↓
    Calculate similarity scores


Step 3: Entity Extraction from Results (Entity Module)
──────────────────────────────────────────────────────
    For each retrieved chunk:
            ↓
    spaCy NER extraction
            ↓
    Collect all entities
            ↓
    Deduplicate (keep unique)
            ↓
    Remove duplicates


Step 4: Graph Extraction (Graph Builder Module)
────────────────────────────────────────────────
    Get entities from retrieval
            ↓
    Query NetworkX graph
            ↓
    Extract subgraph for these entities
            ↓
    Format as Cytoscape JSON


Step 5: Answer Generation (Answer Generator Module)
───────────────────────────────────────────────────
    Prepare prompt:
    
    System: "Answer using ONLY context provided..."
    
    Context: [join retrieved chunks]
    Question: [user query]
            ↓
    Call OpenAI API
            ↓
    Receive answer text
            ↓
    (If no API key: Use heuristic extraction)


Step 6: Response Assembly
──────────────────────────
    Compile response JSON:
    {
        "answer": "generated text",
        "entities": [
            {"name": "Entity1", "type": "PERSON"},
            ...
        ],
        "relationships": [
            {"from_entity": "A", "to_entity": "B", "relation": "type"},
            ...
        ],
        "graph_data": {
            "nodes": [...],
            "edges": [...]
        },
        "snippets": ["chunk1", "chunk2", ...],
        "status": "success"
    }


Step 7: Frontend Rendering
──────────────────────────
    Receive JSON response
            ↓
    Update Zustand store
            ↓
    Render in tabs:
    - Answer tab: Show markdown answer
    - Graph tab: Render Cytoscape graph
    - Entities tab: Show table of entities
    - Snippets: Display source text
```

## Storage Architecture

```
In-Memory Session Storage
──────────────────────────

sessions[uuid] = RAGSession {
    
    session_id: "550e8400-..."
    
    ┌─────────────────────────────────────┐
    │ FAISS Index                         │
    │ - Embeddings (float32, 384-dim)    │
    │ - Metadata pointers                 │
    │ Memory: ~1.5MB per 1000 chunks     │
    └─────────────────────────────────────┘
    
    ┌─────────────────────────────────────┐
    │ Text Chunks Cache                   │
    │ - Original normalized text          │
    │ - Source metadata                   │
    │ - Chunk indices                     │
    │ Memory: ~500KB-1MB per 1000 chunks │
    └─────────────────────────────────────┘
    
    ┌─────────────────────────────────────┐
    │ Entities Dictionary                 │
    │ - Entity name → {type, source}     │
    │ - Chunk → entities mapping         │
    │ Memory: ~100-300KB per 1000 chunks │
    └─────────────────────────────────────┘
    
    ┌─────────────────────────────────────┐
    │ NetworkX Knowledge Graph            │
    │ - Nodes: entities with metadata     │
    │ - Edges: relationships             │
    │ Memory: ~200-500KB per 1000 chunks │
    └─────────────────────────────────────┘
    
    ┌─────────────────────────────────────┐
    │ Retriever Object                    │
    │ - Reference to FAISS index          │
    │ - Access to chunks & sources        │
    └─────────────────────────────────────┘
    
    ┌─────────────────────────────────────┐
    │ Graph Builder Object                │
    │ - Compiled NetworkX graph           │
    │ - Ready for serialization           │
    └─────────────────────────────────────┘
}

Total per session: ~4-6MB per 1000 chunks
```

## Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         API Layer (FastAPI)                      │
│                     request validation & routing                 │
└──────────┬─────────────────────────────────────────┬─────────────┘
           │                                         │
           ▼                                         ▼
    ┌─────────────┐                          ┌──────────────┐
    │ POST /upload │                          │ POST /query  │
    └──────┬──────┘                           └──────┬───────┘
           │                                         │
           ▼                                         ▼
    ┌────────────────────────────┐          ┌──────────────────┐
    │ Preprocessing Module       │          │ Retrieval Module │
    │ ├─ extract_text_from_pdf   │          │ ├─ encode query  │
    │ ├─ clean_text              │          │ └─ faiss.search  │
    │ └─ chunk_text              │          └────────┬─────────┘
    └──────┬─────────────────────┘                   │
           │                                         ▼
           ▼                            ┌──────────────────────┐
    ┌────────────────────────────┐     │ Entity Extraction    │
    │ Retrieval Module           │     │ (on retrieved chunks)│
    │ ├─ EmbeddingModel.encode   │     │ └─ spacy_nlp         │
    │ └─ FAISSRetriever.build    │     └────────┬─────────────┘
    └──────┬─────────────────────┘              │
           │                                    ▼
           ▼                            ┌──────────────────────┐
    ┌────────────────────────────┐     │ Graph Builder        │
    │ Entity Extraction Module   │     │ └─ subgraph query   │
    │ ├─ EntityExtractor.extract │     └────────┬─────────────┘
    │ └─ extract_from_chunks     │             │
    └──────┬─────────────────────┘             ▼
           │                            ┌──────────────────────┐
           ▼                            │ Answer Generator     │
    ┌────────────────────────────┐     │ ├─ openai.api.call   │
    │ Graph Builder Module       │     │ └─ fallback_heuristic│
    │ ├─ build_graph             │     └────────┬─────────────┘
    │ └─ get_graph_data (JSON)   │             │
    └──────┬─────────────────────┘             │
           │                                  │
           └──────────────────────┬───────────┘
                                  ▼
                        ┌────────────────────┐
                        │ Response Assembly  │
                        │ Return JSON        │
                        └────────┬───────────┘
                                 │
                                 ▼
                        Return to Frontend
```

---

This architecture is:
- ✅ **Modular**: Each component has a single responsibility
- ✅ **Scalable**: Can be distributed across services
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Testable**: Each module can be tested independently
- ✅ **Extensible**: Easy to add new components

---

**Last Updated**: January 2026

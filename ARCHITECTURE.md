# Architecture Documentation

## System Design Overview

This document provides comprehensive details about the architecture of the Explainable RAG with Knowledge Graphs application.

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                         │
│                      (React + Vite + Tailwind)                       │
│  ┌──────────────────┬──────────────────┬──────────────────────┐   │
│  │ DocumentUpload   │ QueryForm        │ ResultsPanel         │   │
│  ├──────────────────┼──────────────────┼──────────────────────┤   │
│  │ GraphVisualization (Cytoscape.js)                         │   │
│  │ ErrorAlert       │ Dashboard         │                     │   │
│  └──────────────────┴──────────────────┴──────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────────────┐
│                         API Layer (FastAPI)                         │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐   │
│  │ POST /upload │ POST /query  │ GET /status  │ POST /clear  │   │
│  └──────────────┴──────────────┴──────────────┴──────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Backend Processing Pipeline                      │
│  ┌───────────────┬──────────────┬──────────────┬────────────────┐ │
│  │ Preprocessing │  Retrieval   │  Extraction  │ Graph Builder  │ │
│  │ (Chunking)    │  (FAISS)     │  (spaCy NER) │ (NetworkX)     │ │
│  └───────────────┴──────────────┴──────────────┴────────────────┘ │
│                              ↓                                     │
│              ┌─────────────────────────────────┐                 │
│              │   Answer Generator (OpenAI)     │                 │
│              │   with fallback local inference │                 │
│              └─────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    In-Memory Data Storage                           │
│  ┌──────────────┬──────────────┬──────────────┬────────────────┐ │
│  │  FAISS Index │  Text Chunks │  Embeddings  │  Entity Cache  │ │
│  │  (Per Session)              │              │               │ │
│  └──────────────┴──────────────┴──────────────┴────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 2. Component Breakdown

### 2.1 Frontend Components

#### Dashboard.jsx
**Purpose**: Main layout and state management  
**Responsibilities**:
- Render main UI sections (upload, query, results)
- Tab switching between Answer/Graph/Entities views
- Integration of child components

**State Management**:
- Uses Zustand store (`appStore.js`)
- Global state: `indexId`, `results`, `loading`, `error`

#### DocumentUpload.jsx
**Purpose**: File upload interface  
**Responsibilities**:
- Drag-and-drop file handling
- File selection validation
- API call to `/upload` endpoint
- Progress indication

#### QueryForm.jsx
**Purpose**: Query input and submission  
**Responsibilities**:
- Textarea for natural language queries
- Form validation
- API call to `/query` endpoint
- Loading state management

#### GraphVisualization.jsx
**Purpose**: Interactive graph rendering  
**Responsibilities**:
- Convert graph data to Cytoscape format
- Render interactive knowledge graph
- Node styling and layout
- Edge labeling with relationship types

#### ResultsPanel.jsx
**Purpose**: Results display and actions  
**Responsibilities**:
- Show generated answer
- Display entities in table format
- List source snippets
- Download results as JSON
- Copy answer to clipboard

#### ErrorAlert.jsx
**Purpose**: Error notification  
**Responsibilities**:
- Display error messages
- Auto-dismiss capability
- Global error handling

### 2.2 Backend Modules

#### preprocessing.py
**Purpose**: Document processing and chunking  

**Key Functions**:
- `extract_text_from_pdf()`: Parse PDF files
- `extract_text_from_file()`: Generic file extraction
- `clean_text()`: Text normalization and sanitization
- `chunk_text()`: Split into overlapping chunks

**Parameters**:
- Chunk size: 300 words (configurable)
- Overlap: 50 words
- Supported formats: PDF, TXT, MD

**Output**: List of normalized text chunks with source metadata

#### retrieval.py
**Purpose**: Vector-based semantic search  

**Classes**:
- `EmbeddingModel`: Wraps SentenceTransformers
  - Default model: `all-MiniLM-L6-v2`
  - Dimension: 384
  - Method: `encode(texts) → embeddings`

- `FAISSRetriever`: Manages FAISS index
  - Index type: FlatL2 (Euclidean distance)
  - Methods:
    - `build_index(texts, sources)`: Create index from chunks
    - `retrieve(query, k)`: Get top-k relevant chunks
    - `is_indexed()`: Check if index exists

**Performance**:
- Embedding: ~100ms per chunk
- Retrieval: ~50ms per query
- Memory: ~1.2MB per 1000 chunks

#### entity_extraction.py
**Purpose**: Named entity recognition  

**Classes**:
- `EntityExtractor`: spaCy-based NER
  - Model: `en_core_web_sm`
  - Recognized types: PERSON, ORG, LOC, GPE, PRODUCT, EVENT, etc.
  - Methods:
    - `extract_entities(text)`: Single chunk extraction
    - `extract_from_chunks(chunks)`: Batch extraction
    - `extract_noun_phrases(text)`: Noun phrase extraction

**Output**: List of entities with type and source chunk

#### graph_builder.py
**Purpose**: Knowledge graph construction  

**Classes**:
- `KnowledgeGraphBuilder`: NetworkX-based graph management
  - Nodes: Entity names with metadata (type, source)
  - Edges: Relationships with types (co-occurs, verb-based)
  - Methods:
    - `build_graph()`: Construct from entities and chunks
    - `get_graph_data()`: Convert to Cytoscape format
    - `get_relationships()`: Extract edge information

**Graph Construction Logic**:
1. Add all unique entities as nodes
2. For each chunk:
   - Find entities in same chunk
   - Add edges between co-occurring entities
   - Label: "co-occurs-in-chunk"
3. If spaCy available:
   - Parse dependencies
   - Add verb-based edges (e.g., "developed", "created")

**Output**: Cytoscape-compatible JSON with nodes and edges

#### answer_generator.py
**Purpose**: LLM-based answer generation  

**Classes**:
- `AnswerGenerator`: LLM integration with fallback
  - Primary: OpenAI API (gpt-4o-mini)
  - Fallback: Heuristic extraction
  - Methods:
    - `generate(query, context_chunks)`: Generate answer
    - `_generate_fallback()`: No-LLM alternative

**Prompt Template**:
```
System: You are helpful assistant. Answer using ONLY provided context.
        Do not hallucinate.

User: Context:
      [Retrieved chunks joined]
      
      Question: [User query]
      
      Answer:
```

**Constraints**:
- Context limited to 4000 tokens
- Temperature: 0.3 (low randomness)
- Max tokens: 500

### 2.3 API Layer

#### Endpoints Design

**POST /upload**
- Input: MultipartForm with files
- Process:
  1. Read files (memory-limited to 100MB total)
  2. Extract text → chunks
  3. Embed chunks → FAISS index
  4. Extract entities → cache
  5. Build knowledge graph
- Output: Session ID, chunk count
- Storage: In-memory `sessions` dict

**POST /query**
- Input: Query string + session ID
- Process:
  1. Retrieve top-5 relevant chunks
  2. Extract entities from retrieved chunks
  3. Generate answer with LLM
  4. Build response graph
- Output: Answer + Entities + Graph + Snippets

**GET /status**
- Input: None
- Output: Health status

**POST /clear**
- Input: Session ID
- Output: Confirmation

#### Session Management

```python
class RAGSession:
    - session_id: str (UUID)
    - retriever: FAISSRetriever
    - chunks: List[str]
    - sources: List[str]
    - entities: List[Dict]
    - entity_chunk_map: Dict
    - graph_builder: KnowledgeGraphBuilder
```

Sessions stored in global dict (in-memory):
```python
sessions[session_id] = RAGSession(session_id)
```

**Limitations**:
- Sessions lost on restart
- No concurrent session isolation
- Memory accumulates with multiple sessions

**For Production**:
- Use Redis or PostgreSQL
- Implement garbage collection
- Add session timeout

## 3. Data Flow Diagrams

### 3.1 Document Upload Flow

```
User selects files
        ↓
Frontend: POST /upload
        ↓
Backend: Read files → Extract text
        ↓
Preprocess: Clean, split into chunks
        ↓
Embedding: Encode chunks to vectors
        ↓
FAISS: Build index from vectors
        ↓
NER: Extract entities from chunks
        ↓
GraphBuilder: Create entity relationships
        ↓
Response: Return session ID + metadata
        ↓
Frontend: Display success message
```

### 3.2 Query Processing Flow

```
User enters query + submits
        ↓
Frontend: POST /query {query, index_id}
        ↓
Backend: Embed query
        ↓
FAISS: Retrieve top-5 chunks (similarity search)
        ↓
NER: Extract entities from retrieved chunks
        ↓
LLM: Generate answer with context
        ↓
GraphBuilder: Build subgraph for retrieved entities
        ↓
Format: Compile answer + entities + graph
        ↓
Response: Return JSON
        ↓
Frontend: Render answer, graph, entities
```

### 3.3 Storage Architecture

```
┌─────────────────────────────────────────┐
│         Session Container               │
│  (In-Memory, Per Session)               │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  FAISS Index (Binary)          │   │
│  │  - Embedding vectors (float32) │   │
│  │  - Size: ~1.5MB per 1000 chunks│   │
│  └────────────────────────────────┘   │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  Chunk Cache (List)            │   │
│  │  - Original text (UTF-8)       │   │
│  │  - Source metadata             │   │
│  └────────────────────────────────┘   │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  Entity Cache (Dict)           │   │
│  │  - Extracted entities          │   │
│  │  - Entity → Chunk mapping      │   │
│  └────────────────────────────────┘   │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  NetworkX Graph (Graph obj)    │   │
│  │  - Nodes: entities             │   │
│  │  - Edges: relationships        │   │
│  └────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## 4. Performance Characteristics

### 4.1 Processing Times (Benchmarks)

| Operation | Time | Notes |
|-----------|------|-------|
| Upload 5 files (1.5MB total) | 10-15s | Includes chunking, embedding |
| Embed single chunk (300 words) | ~100ms | SentenceTransformers |
| FAISS search (k=5) | ~50ms | Cosine similarity |
| NER on chunk | ~200ms | spaCy pipeline |
| Query → Answer | 3-10s | Mostly LLM API latency |
| **Total end-to-end query** | **3-10s** | Depends on LLM |

### 4.2 Memory Usage

| Component | Per 1000 Chunks | Per 10000 Chunks |
|-----------|-----------------|------------------|
| FAISS Index | ~1.5MB | ~15MB |
| Text Cache | ~500KB-1MB | ~5-10MB |
| Embeddings (cached) | ~1.5MB | ~15MB |
| Entity Cache | ~100-300KB | ~1-3MB |
| NetworkX Graph | ~200-500KB | ~2-5MB |
| **Total** | **~4-6MB** | **~40-60MB** |

## 5. Security Architecture

### 5.1 Input Validation

**File Upload**:
- Accepted types: PDF, TXT, MD only
- Max size: 100MB per file (enforce in production)
- File validation: Check MIME type

**Query Input**:
- Min length: 1 character
- Max length: 1000 characters
- Sanitization: Pydantic models handle escaping

### 5.2 Data Isolation

- No persistent storage by default (memory-only)
- Sessions isolated by UUID
- No cross-session data leakage
- No authentication by default (add for multi-user)

### 5.3 CORS & API Security

**Current CORS Policy**:
```python
allow_origins=["*"]  # ⚠️ For development only
```

**For Production**:
```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

## 6. Scalability Considerations

### 6.1 Horizontal Scaling

Current architecture supports:
- Single process, single machine
- Limited by RAM for in-memory storage
- ~100k chunks max on 8GB RAM

For scaling:

1. **Session Persistence**:
   ```
   Redis: Store FAISS indices
   PostgreSQL: Store chunks, entities, graphs
   ```

2. **Async Processing**:
   ```
   Celery: Queue long-running uploads
   Message Broker: RabbitMQ
   ```

3. **Load Balancing**:
   ```
   Nginx: Distribute requests
   Multiple API instances
   Sticky sessions (if needed)
   ```

### 6.2 Vertical Scaling

- Use GPU-accelerated FAISS: `faiss-gpu`
- Use larger embedding models
- Increase chunk size (for fewer embeddings)

## 7. Error Handling

### 7.1 Backend Error Handling

```python
try:
    # Main processing
except HTTPException:
    raise  # Re-raise HTTP exceptions
except Exception as e:
    # Log error
    raise HTTPException(status_code=500, detail=str(e))
```

### 7.2 Frontend Error Handling

```javascript
try {
    const result = await api.post('/query', data);
} catch (err) {
    setError(err.response?.data?.detail || 'Failed');
}
```

## 8. Testing Strategy

### 8.1 Unit Tests

- **preprocessing.py**: Text cleaning, chunking
- **retrieval.py**: Embedding, FAISS operations
- **entity_extraction.py**: NER accuracy
- **graph_builder.py**: Graph construction
- Location: `backend/tests/`

### 8.2 Integration Tests

- Upload → Retrieval → Query flow
- End-to-end API tests

### 8.3 Performance Tests

- Embedding latency
- FAISS search time
- Memory usage

## 9. Deployment Architecture

### 9.1 Docker Containerization

**Backend Image**:
- Base: `python:3.12-slim`
- Size: ~800MB (with dependencies)
- Includes spaCy model

**Frontend Image**:
- Build stage: Node 20 + build tools
- Runtime stage: Node 20 + serve
- Size: ~200MB

### 9.2 Compose Configuration

```yaml
services:
  backend:
    build: Dockerfile.backend
    ports: 8000
    healthcheck: /status endpoint
    
  frontend:
    build: Dockerfile.frontend
    ports: 3000
    depends_on: backend
```

### 9.3 Environment Variables

```env
OPENAI_API_KEY=sk-...
VITE_API_URL=http://localhost:8000
```

## 10. Future Architecture Improvements

### 10.1 Caching Layer
```
Redis Cache
  - Embeddings (prevent recomputation)
  - Query results
  - Entity cache
```

### 10.2 Database Integration
```
PostgreSQL
  - Persistent indices
  - User sessions
  - Query history
  - Document metadata
```

### 10.3 Advanced Features
```
- Vector database (Pinecone, Weaviate)
- Full-text search (Elasticsearch)
- Advanced caching (Memcached)
- Message queue (Kafka)
- Monitoring (Prometheus, Grafana)
```

---

**Document Version**: 1.0.0  
**Last Updated**: January 2026

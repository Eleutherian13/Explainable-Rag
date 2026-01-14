# Copilot Instructions for Dataforge Project

These instructions provide guidance for working with the Explainable RAG with Knowledge Graphs web application.

## Project Overview

**Dataforge** is a modern full-stack web application implementing Retrieval-Augmented Generation (RAG) with knowledge graph-based explanations. Users can upload documents, ask questions, and receive grounded answers with visual knowledge graphs.

- **Backend**: FastAPI + Python (RAG pipeline)
- **Frontend**: React + Vite (User interface)
- **Deployment**: Docker + Docker Compose
- **Tech**: FAISS, spaCy, NetworkX, OpenAI API

## Architecture

```
User Interface (React)
         ↓
    API Layer (FastAPI)
         ↓
Core Pipeline:
  1. Document Preprocessing (chunking, embedding)
  2. Vector Retrieval (FAISS)
  3. Entity Extraction (spaCy NER)
  4. Knowledge Graph Construction (NetworkX)
  5. Answer Generation (OpenAI/HF)
  6. Visualization (Cytoscape)
```

## Key Directories

- **backend/app/main.py**: FastAPI application and endpoints
- **backend/app/modules/**: Core RAG pipeline modules
  - `preprocessing.py`: Document chunking and cleaning
  - `retrieval.py`: Embedding and FAISS vector search
  - `entity_extraction.py`: Named entity recognition
  - `graph_builder.py`: Knowledge graph construction
  - `answer_generator.py`: LLM integration
- **frontend/src/components/**: React components
  - `Dashboard.jsx`: Main application layout
  - `DocumentUpload.jsx`: File upload interface
  - `QueryForm.jsx`: Query submission
  - `GraphVisualization.jsx`: Cytoscape graph rendering
  - `ResultsPanel.jsx`: Results display

## API Endpoints

1. **POST /upload**: Upload and index documents
2. **POST /query**: Submit query, receive answer with explanations
3. **GET /status**: Health check
4. **POST /clear**: Clear session

See README.md for detailed API documentation.

## Common Tasks

### Running the Application

**Docker (Recommended)**:

```bash
docker-compose up
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

**Local Development**:

```bash
# Terminal 1: Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm install && npm run dev
```

### Adding Features

**New Backend Endpoint**:

1. Add schema in `backend/app/models/schemas.py`
2. Create handler in `backend/app/main.py`
3. Add tests in `backend/tests/`

**New Frontend Component**:

1. Create component in `frontend/src/components/`
2. Import in relevant parent component
3. Add to dashboard if needed

### Debugging

**Backend**:

- Check logs: `docker-compose logs backend`
- FastAPI docs: http://localhost:8000/docs
- Run tests: `cd backend && pytest -v`

**Frontend**:

- Browser DevTools (F12)
- Check API responses in Network tab
- React Developer Tools browser extension

### Code Quality

**Backend**:

```bash
cd backend
black . --check && ruff check .
```

**Frontend**:

```bash
cd frontend
npm run lint
```

## Configuration

- **OpenAI API Key**: Set in `.env` file
- **Embedding Model**: Change in `answer_generator.py` (default: `all-MiniLM-L6-v2`)
- **LLM Model**: Change in `answer_generator.py` (default: `gpt-4o-mini`)
- **Chunk Size**: Modify in `preprocessing.py` (default: 300 words)

## Performance Considerations

- **Embedding**: ~100ms per chunk
- **Retrieval**: ~50ms FAISS search
- **Answer Generation**: 2-5s (API dependent)
- **Total Latency**: 3-10s per query

For large corpora, consider:

- Adding Redis for embedding caching
- Using GPU-accelerated FAISS (`faiss-gpu`)
- Implementing result pagination
- Adding database persistence (PostgreSQL)

## Testing

```bash
# Backend tests
cd backend && pytest

# Run specific test
pytest tests/test_preprocessing.py::TestChunking::test_chunk_text_basic
```

## Deployment

### Docker Build

```bash
docker build -f Dockerfile.backend -t rag-backend .
docker build -f Dockerfile.frontend -t rag-frontend .
```

### Production Deployment

1. **Add authentication**: JWT in FastAPI
2. **Environment variables**: Use secrets manager
3. **Database**: PostgreSQL for persistence
4. **Caching**: Redis for embeddings
5. **Monitoring**: Add logging and error tracking
6. **Scaling**: Use load balancers, message queues

## Troubleshooting Checklist

- [ ] Python 3.12+ installed
- [ ] Node.js 20+ installed
- [ ] Docker running
- [ ] OpenAI API key set (if using LLM)
- [ ] Port 8000 and 3000 available
- [ ] `spacy` model downloaded: `python -m spacy download en_core_web_sm`
- [ ] Dependencies installed: `pip install -r requirements.txt`

## Code Style

- **Python**: Black formatter, Ruff linter
- **JavaScript**: Prettier formatter
- **Component naming**: PascalCase for React components
- **Function naming**: camelCase for functions
- **Constants**: UPPER_SNAKE_CASE

## Git Workflow

```bash
# Feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Add feature description"

# Push and create PR
git push origin feature/my-feature
```

## Security Notes

- No persistent storage by default (in-memory)
- CORS configured for localhost
- Input validation via Pydantic
- Session isolation per upload
- No sensitive data in logs

## Important Files Not to Modify

- `docker-compose.yml`: Use env vars for config
- `package.json`: Update via `npm install`
- `requirements.txt`: Update via `pip freeze`

## Useful Commands

```bash
# View running containers
docker ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild without cache
docker-compose build --no-cache

# Run tests
cd backend && pytest -v --cov

# Format code
black backend/app
```

## Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev
- FAISS: https://github.com/facebookresearch/faiss
- spaCy: https://spacy.io/
- NetworkX: https://networkx.org/
- Cytoscape.js: https://js.cytoscape.org/

## Questions?

1. Check README.md for detailed documentation
2. Review GETTING_STARTED.md for setup help
3. Inspect source code comments
4. Check test files for usage examples

---

**Project Status**: Production Ready (v1.0.0)  
**Last Updated**: January 2026

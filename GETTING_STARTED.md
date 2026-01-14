# Getting Started Guide

## Project Overview

This is a complete web application implementing **Explainable RAG with Knowledge Graphs**. The system allows users to upload documents, ask questions in natural language, and receive answers grounded in the source documents with visual knowledge graphs showing entity relationships.

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended for quick setup)
- **Python 3.12+** (for local backend development)
- **Node.js 20+** (for local frontend development)
- **OpenAI API Key** (optional, for LLM-powered answers)

## 🚀 Quick Start (Docker - Recommended)

### 1. Navigate to Project

```bash
cd c:\Users\manas\OneDrive\Desktop\Dataforge
```

### 2. Setup Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your OpenAI API key (optional)
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Start Services

```bash
# Build and start both frontend and backend
docker-compose up

# On first run, this will:
# - Install Python dependencies and download spaCy model
# - Install Node.js dependencies
# - Start FastAPI backend on http://localhost:8000
# - Start React frontend on http://localhost:3000
```

### 4. Access Application

- **Frontend**: http://localhost:3000 (or http://localhost:3000)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 💻 Local Development Setup

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# or (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start backend server
uvicorn app.main:app --reload --port 8000
```

**Backend will run at**: http://localhost:8000

### Frontend Setup

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will run at: http://localhost:5173
```

Configure API URL in `frontend/src/services/api.js` if needed.

## 📖 First Steps with the Application

### 1. Upload Documents

1. Go to "Upload Documents" section
2. Drag and drop PDF, TXT, or Markdown files
3. Click "Upload & Index Documents"
4. Wait for success message (shows index ID and chunk count)

### 2. Ask a Question

1. In "Ask a Question" section, type your query
2. Click "Submit Query"
3. Wait for processing (usually 3-10 seconds)

### 3. View Results

Results appear in tabs:

- **Answer**: AI-generated answer grounded in documents
- **Knowledge Graph**: Visual representation of entity relationships
- **Entities**: Extracted entities (people, organizations, locations, etc.)
- Plus source snippets showing where information came from

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest
```

### Run Backend Linting

```bash
cd backend
black . --check
ruff check .
```

## 📁 Project Structure Quick Reference

```
Dataforge/
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── main.py        # API endpoints
│   │   ├── models/        # Pydantic schemas
│   │   └── modules/       # Core RAG pipeline
│   ├── tests/             # Unit tests
│   └── requirements.txt
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── store/         # Zustand state
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml     # Multi-container setup
├── .env.example          # Environment template
└── README.md             # Full documentation
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/app/main.py`:

- Embedding model: `all-MiniLM-L6-v2` (line ~20)
- LLM model: `gpt-4o-mini` (line ~21)
- Default retrieval k: `5`

Edit `backend/app/modules/preprocessing.py`:

- Chunk size: `300` words (line ~61)
- Chunk overlap: `50` words (line ~61)

### Frontend Configuration

Edit `frontend/src/services/api.js`:

- API base URL: `http://localhost:8000` (line ~3)

Edit `frontend/.env` (if needed):

```
VITE_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'spacy'"**

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Port 8000 already in use**

```bash
# Change port in docker-compose.yml or use:
uvicorn app.main:app --port 8001
```

**High memory usage**

- Reduce chunk size in preprocessing.py
- Clear old sessions via `/clear` endpoint
- Limit file upload sizes

### Frontend Issues

**Cannot connect to API**

1. Check backend is running: `curl http://localhost:8000/status`
2. Check CORS in `backend/app/main.py` (should allow all origins)
3. Verify API URL in `frontend/src/services/api.js`

**Module not found**

```bash
cd frontend
npm install
npm run dev
```

### Docker Issues

**Build fails with "No space left on device"**

```bash
docker system prune -a
docker-compose build --no-cache
```

**Container exits immediately**

```bash
docker-compose logs backend
docker-compose logs frontend
```

## 📊 Example Workflow

### Upload Sample Documents

```bash
# Create a sample document
echo "Python is a programming language created by Guido van Rossum in 1991. It is used for web development, data science, and artificial intelligence." > sample.txt

# Upload via UI or API
curl -F "files=@sample.txt" http://localhost:8000/upload
```

### Submit Query

```bash
# Using the browser UI:
# Type: "Who created Python?"
# Result: "Python was created by Guido van Rossum"
# Graph shows: Guido van Rossum → created → Python
```

## 🎯 Next Steps

1. **Customize LLM**: Change from OpenAI to HuggingFace models in `answer_generator.py`
2. **Add Authentication**: Implement JWT in FastAPI
3. **Scale Storage**: Add PostgreSQL for persistent indices
4. **Deploy**: Push to Docker Hub, deploy on Heroku/AWS/GCP
5. **Monitor**: Add logging and monitoring via ELK stack

## 📚 Additional Resources

- **FastAPI Docs**: http://localhost:8000/docs (when running)
- **React Documentation**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Cytoscape.js**: https://js.cytoscape.org

## 💡 Tips

- **GPU Acceleration**: For faster embeddings on large corpora, use `faiss-gpu` instead of `faiss-cpu`
- **Model Caching**: Embeddings are computed fresh each session; add Redis caching for scale
- **API Rate Limiting**: Add rate limiting middleware for production
- **Error Tracking**: Integrate Sentry for error monitoring

## ✉️ Support

If stuck:

1. Check full README.md for detailed API docs
2. Review logs: `docker-compose logs -f backend`
3. Check browser DevTools (F12) for frontend errors
4. Verify OpenAI API key format if using LLM features

---

**Happy exploring!** 🚀

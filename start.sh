#!/bin/bash
# Quick start script for Explainable RAG application

set -e

echo "================================"
echo "Explainable RAG - Quick Start"
echo "================================"
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop."
    exit 1
fi

echo "✅ Docker found"

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Desktop."
    exit 1
fi

echo "✅ Docker Compose found"

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OpenAI API key if desired"
    echo "   Then run this script again"
    echo ""
    echo "To get your OpenAI API key:"
    echo "  1. Go to https://platform.openai.com/account/api-keys"
    echo "  2. Create a new secret key"
    echo "  3. Add it to .env: OPENAI_API_KEY=sk-..."
    exit 0
fi

echo "✅ .env file found"

# Stop any existing containers
echo ""
echo "🛑 Stopping any existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true

# Build images
echo ""
echo "🔨 Building Docker images..."
echo "   This may take 2-5 minutes on first run..."
docker-compose build

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Check if services are running
echo ""
echo "🔍 Checking service status..."

backend_healthy=false
frontend_ready=false
attempts=0

while [ $attempts -lt 30 ]; do
    attempts=$((attempts + 1))
    
    # Check backend
    if curl -s http://localhost:8000/status > /dev/null 2>&1; then
        backend_healthy=true
    fi
    
    # Check if frontend container is running
    if docker ps | grep -q "rag-frontend"; then
        frontend_ready=true
    fi
    
    if [ "$backend_healthy" = true ] && [ "$frontend_ready" = true ]; then
        break
    fi
    
    echo "  Attempt $attempts/30: Waiting for services..."
    sleep 2
done

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""

if [ "$backend_healthy" = true ]; then
    echo "✅ Backend API is running"
    echo "   📍 API: http://localhost:8000"
    echo "   📖 Docs: http://localhost:8000/docs"
else
    echo "⚠️  Backend still starting, please wait..."
fi

if [ "$frontend_ready" = true ]; then
    echo "✅ Frontend is running"
    echo "   🌐 URL: http://localhost:3000"
else
    echo "⚠️  Frontend still starting, please wait..."
fi

echo ""
echo "🎯 Next Steps:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Upload some documents (PDF, TXT, or MD files)"
echo "  3. Ask a question about the documents"
echo "  4. View the knowledge graph and explanations"
echo ""
echo "📚 Documentation:"
echo "  - Full guide: README.md"
echo "  - Getting started: GETTING_STARTED.md"
echo "  - View logs: docker-compose logs -f"
echo ""
echo "🛑 To stop:"
echo "  docker-compose down"
echo ""
echo "Happy exploring! 🚀"

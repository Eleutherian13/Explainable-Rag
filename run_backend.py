#!/usr/bin/env python
"""Simple backend startup script."""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting Dataforge Backend Server...")
    print("📍 Server will run on http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("❌ Press CTRL+C to stop\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

#!/bin/bash

# AI Chatbot System - Backend Runner Script

echo "🚀 Starting AI Chatbot System Backend..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping services..."
    docker-compose down
    echo "✅ Services stopped."
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Start PostgreSQL first
echo "📦 Starting PostgreSQL..."
docker-compose up postgres -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker-compose exec -T postgres pg_isready -U user -d ai_qa_db; do
    echo "⏳ PostgreSQL is not ready yet. Waiting..."
    sleep 2
done
echo "✅ PostgreSQL is ready!"

# Start the backend
echo "🔧 Starting FastAPI Backend..."
docker-compose up backend

echo "🎉 Backend is running!"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health" 
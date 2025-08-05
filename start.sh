#!/bin/bash

# AI Question Answering System Startup Script

echo "🚀 Starting AI Question Answering System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
    echo "📝 Please edit .env file and add your OpenAI API key before starting the application."
    echo "   You can get an API key from: https://platform.openai.com/api-keys"
    exit 1
fi

# Check if OpenAI API key is set
if grep -q "your-openai-api-key-here" .env; then
    echo "❌ Please set your OpenAI API key in the .env file before starting."
    echo "   You can get an API key from: https://platform.openai.com/api-keys"
    exit 1
fi

echo "✅ Environment check passed!"

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Build and start the application
echo "🔨 Building and starting the application..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Application started successfully!"
    echo ""
    echo "🌐 Access the application:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📝 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Failed to start application. Check logs with: docker-compose logs"
    exit 1
fi 
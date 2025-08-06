#!/bin/bash

echo "🚀 Starting AI Question Answering System (Local Development)"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check if PostgreSQL is running
echo "🗄️  Checking PostgreSQL..."
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running on localhost:5432"
    echo "   Please start PostgreSQL and create a database named 'ai_qa_db'"
    echo "   Then update the DATABASE_URL in backend/.env"
fi

# Set up backend
echo "🔧 Setting up backend..."
cd backend

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit backend/.env with your configuration"
    echo "   - Set your OpenAI API key"
    echo "   - Update DATABASE_URL if needed"
    echo "   - Set a secure SECRET_KEY"
fi

# Start backend in background
echo "🚀 Starting backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Set up frontend
echo "🔧 Setting up frontend..."
cd ../frontend

# Install dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Start frontend in background
echo "🚀 Starting frontend server..."
npm start &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

echo ""
echo "🎉 Application started successfully!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "🛑 To stop the application:"
echo "   Press Ctrl+C or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📝 To view logs:"
echo "   Backend logs will appear in this terminal"
echo "   Frontend logs will appear in a new terminal window"

# Wait for user to stop
wait 
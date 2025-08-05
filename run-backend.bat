@echo off
echo 🚀 Starting AI Chatbot System Backend...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo 📦 Starting PostgreSQL...
docker-compose up postgres -d

echo ⏳ Waiting for PostgreSQL to be ready...
:wait_loop
docker-compose exec -T postgres pg_isready -U user -d ai_qa_db >nul 2>&1
if errorlevel 1 (
    echo ⏳ PostgreSQL is not ready yet. Waiting...
    timeout /t 2 /nobreak >nul
    goto wait_loop
)
echo ✅ PostgreSQL is ready!

echo 🔧 Starting FastAPI Backend...
docker-compose up backend

echo 🎉 Backend is running!
echo 📖 API Documentation: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/health
pause 
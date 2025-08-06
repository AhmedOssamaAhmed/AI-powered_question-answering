@echo off
echo 🚀 Starting AI Question Answering System (Local Development)

echo 📋 Checking prerequisites...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm
    pause
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

echo 🗄️  Starting PostgreSQL with Docker...
docker-compose up -d postgres

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 10 /nobreak >nul

REM Check if PostgreSQL is running
docker-compose ps postgres | findstr "Up" >nul
if errorlevel 1 (
    echo ❌ Failed to start PostgreSQL. Please check:
    echo    - Docker Desktop is running
    echo    - Port 5432 is not already in use
    echo    - Docker has enough resources allocated
    pause
    exit /b 1
)

echo ✅ PostgreSQL is running on localhost:5432
echo    Database: ai_qa_db | User: user | Password: password

echo 🔧 Setting up backend...
cd backend

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit backend/.env with your configuration
    echo    - Set your OpenAI API key (required)
    echo    - DATABASE_URL is automatically configured for Docker
    echo    - Set a secure SECRET_KEY
)

REM Start backend in background
echo 🚀 Starting backend server...
start "Backend Server" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo 🔧 Setting up frontend...
cd ..\frontend

REM Install dependencies
echo 📥 Installing Node.js dependencies...
npm install

REM Start frontend in background
echo 🚀 Starting frontend server...
start "Frontend Server" cmd /k "npm start"

REM Wait a moment for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo 🎉 Application started successfully!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo 🛑 To stop the application:
echo    Close the terminal windows that opened
echo.
echo 📝 To view logs:
echo    Check the terminal windows that opened for backend and frontend logs

pause 
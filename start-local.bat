@echo off
setlocal enabledelayedexpansion

echo 🚀 Starting AI Question Answering System (Local Development)

:: Function to check if a command exists
echo 📋 Checking prerequisites...

where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+
    pause
    exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+
    pause
    exit /b 1
)

where npm >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm
    pause
    exit /b 1
)

where docker >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

:: Start PostgreSQL
echo 🗄️  Starting PostgreSQL with Docker...
docker-compose up -d postgres

echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 10 /nobreak >nul

docker-compose ps postgres | findstr "Up" >nul
if errorlevel 1 (
    echo ❌ Failed to start PostgreSQL. Please check Docker is running and port 5432 is free.
    pause
    exit /b 1
)

echo ✅ PostgreSQL is running on localhost:5432
@REM echo    Database: ai_qa_db | User: user | Password: password

:: Setup backend
echo 🔧 Setting up backend...
cd backend

if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

echo 🔌 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 📥 Installing Python dependencies...
pip install -r requirements.txt

if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy env.example .env >nul
    echo ⚠️  Please edit backend/.env with your configuration
    echo    - Set your OpenAI API key
    echo    - DATABASE_URL is auto-configured for Docker
    echo    - Set a secure SECRET_KEY
)

echo 🚀 Starting backend server...
start "Backend Server" cmd /k "cd /d %cd% && call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

cd ..

:: Setup frontend
echo 🔧 Setting up frontend...
cd frontend

echo 📥 Installing Node.js dependencies...
call :safe_npm_install

if errorlevel 1 (
    echo ⚠️ npm install encountered issues, continuing anyway...
) else (
    echo ✅ Node.js dependencies installed
)

echo 🚀 Starting frontend server...
start "Frontend Server" cmd /k "cd /d %cd% && npm start"

cd ..

timeout /t 50 /nobreak >nul

echo.
echo 🎉 Application started successfully!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo 🛑 To stop the application:
echo    Close the terminal windows that opened (Backend Server and Frontend Server)
echo.
echo 📝 To view logs:
echo    Backend logs: in the Backend Server window
echo    Frontend logs: in the Frontend Server window
:safe_npm_install
    npm install --no-audit --legacy-peer-deps >nul 2>&1
    exit /b 0
pause

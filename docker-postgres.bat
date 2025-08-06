@echo off
echo AI Chatbot System - PostgreSQL Docker Management
echo ===============================================

if "%1"=="start" (
    echo Starting PostgreSQL container...
    docker-compose up -d postgres
    echo.
    echo PostgreSQL is starting up...
    echo You can check the status with: docker-compose ps
    echo.
    echo Connection details:
    echo - Host: localhost
    echo - Port: 5432
    echo - Database: ai_qa_db
    echo - Username: user
    echo - Password: password
    echo.
    echo Database URL: postgresql://user:password@localhost:5432/ai_qa_db
) else if "%1"=="stop" (
    echo Stopping PostgreSQL container...
    docker-compose down
    echo PostgreSQL container stopped.
) else if "%1"=="restart" (
    echo Restarting PostgreSQL container...
    docker-compose restart postgres
    echo PostgreSQL container restarted.
) else if "%1"=="logs" (
    echo Showing PostgreSQL logs...
    docker-compose logs postgres
) else if "%1"=="status" (
    echo Checking PostgreSQL container status...
    docker-compose ps
) else if "%1"=="reset" (
    echo WARNING: This will delete all data!
    set /p confirm="Are you sure you want to reset the database? (y/N): "
    if /i "%confirm%"=="y" (
        echo Stopping and removing PostgreSQL container and data...
        docker-compose down -v
        echo PostgreSQL data has been reset.
    ) else (
        echo Reset cancelled.
    )
) else (
    echo Usage: docker-postgres.bat [command]
    echo.
    echo Commands:
    echo   start   - Start PostgreSQL container
    echo   stop    - Stop PostgreSQL container
    echo   restart - Restart PostgreSQL container
    echo   logs    - Show PostgreSQL logs
    echo   status  - Check container status
    echo   reset   - Reset database (delete all data)
    echo.
    echo Example: docker-postgres.bat start
) 
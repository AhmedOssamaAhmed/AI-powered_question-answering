#!/bin/bash

echo "AI Chatbot System - PostgreSQL Docker Management"
echo "==============================================="

case "$1" in
    "start")
        echo "Starting PostgreSQL container..."
        docker-compose up -d postgres
        echo ""
        echo "PostgreSQL is starting up..."
        echo "You can check the status with: docker-compose ps"
        echo ""
        echo "Connection details:"
        echo "- Host: localhost"
        echo "- Port: 5432"
        echo "- Database: ai_qa_db"
        echo "- Username: user"
        echo "- Password: password"
        echo ""
        echo "Database URL: postgresql://user:password@localhost:5432/ai_qa_db"
        ;;
    "stop")
        echo "Stopping PostgreSQL container..."
        docker-compose down
        echo "PostgreSQL container stopped."
        ;;
    "restart")
        echo "Restarting PostgreSQL container..."
        docker-compose restart postgres
        echo "PostgreSQL container restarted."
        ;;
    "logs")
        echo "Showing PostgreSQL logs..."
        docker-compose logs postgres
        ;;
    "status")
        echo "Checking PostgreSQL container status..."
        docker-compose ps
        ;;
    "reset")
        echo "WARNING: This will delete all data!"
        read -p "Are you sure you want to reset the database? (y/N): " confirm
        if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
            echo "Stopping and removing PostgreSQL container and data..."
            docker-compose down -v
            echo "PostgreSQL data has been reset."
        else
            echo "Reset cancelled."
        fi
        ;;
    *)
        echo "Usage: ./docker-postgres.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start   - Start PostgreSQL container"
        echo "  stop    - Stop PostgreSQL container"
        echo "  restart - Restart PostgreSQL container"
        echo "  logs    - Show PostgreSQL logs"
        echo "  status  - Check container status"
        echo "  reset   - Reset database (delete all data)"
        echo ""
        echo "Example: ./docker-postgres.sh start"
        ;;
esac 
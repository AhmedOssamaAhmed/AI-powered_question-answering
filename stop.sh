#!/bin/bash

# AI Question Answering System Stop Script

echo "🛑 Stopping AI Question Answering System..."

# Stop all containers
docker-compose down

echo "✅ Application stopped successfully!"

# Optional: Remove volumes (uncomment if you want to clear all data)
# echo "🗑️  Removing volumes..."
# docker-compose down -v
# echo "✅ All data cleared!" 
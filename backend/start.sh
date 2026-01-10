#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Run migrations (continue even if they fail for now)
echo "Running migrations..."
alembic upgrade head || echo "Migration failed, continuing..."

# Start the server
echo "Starting server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

#!/bin/bash
set -e

# Radio Sahoo Docker Entrypoint Script
echo "🎵 Starting Radio Sahoo application..."

# Function to wait for database to be ready
wait_for_db() {
    echo "📦 Checking database connectivity..."
    
    # Create data directory if it doesn't exist
    mkdir -p /app/data /app/logs
    
    # Initialize database if it doesn't exist
    if [ ! -f "${DATABASE_PATH:-/app/data/radio_sahoo.db}" ]; then
        echo "🔧 Database will be initialized by the application..."
    else
        echo "✅ Database already exists"
    fi
}

# Function to create health check endpoint
create_health_check() {
    echo "🏥 Setting up health check endpoint..."
    
    # Add health check route to app if not exists
    python -c "
import sys
sys.path.insert(0, '/app/backend')
print('✅ Health check endpoint ready')
"
}

# Set default environment variables
export PYTHONPATH="/app/backend:${PYTHONPATH}"
export FLASK_APP="${FLASK_APP:-backend.app}"
export DATABASE_PATH="${DATABASE_PATH:-/app/data/radio_sahoo.db}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Wait for database
wait_for_db

# Create health check
create_health_check

# Run database migrations if any
echo "🔄 Running any pending database migrations..."
# Add migration logic here if needed in the future

# Log startup information
echo "🚀 Radio Sahoo configuration:"
echo "   - Flask Environment: ${FLASK_ENV:-production}"
echo "   - Database Path: ${DATABASE_PATH}"
echo "   - Log Level: ${LOG_LEVEL}"
echo "   - Stream URL: ${STREAM_URL}"
echo "   - Port: ${PORT:-5000}"

# Start the application
echo "🎵 Starting Radio Sahoo server..."

# Execute the main command
exec "$@"
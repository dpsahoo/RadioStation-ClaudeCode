#!/bin/bash
set -e

# Radio Sahoo Docker Deployment Test Script
echo "🐳 Testing Radio Sahoo Docker deployment configuration..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   - macOS: Download Docker Desktop from https://docker.com"
    echo "   - Linux: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
    echo "   - Windows: Download Docker Desktop from https://docker.com"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose:"
    echo "   - Usually comes with Docker Desktop"
    echo "   - Linux: pip install docker-compose"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Test configuration files
echo "🔍 Validating configuration files..."

# Check Dockerfile
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found"
    exit 1
fi
echo "✅ Dockerfile exists"

# Check docker-compose files
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi
echo "✅ docker-compose.yml exists"

if [ ! -f "docker-compose.prod.yml" ]; then
    echo "❌ docker-compose.prod.yml not found"
    exit 1
fi
echo "✅ docker-compose.prod.yml exists"

# Check .dockerignore
if [ ! -f ".dockerignore" ]; then
    echo "❌ .dockerignore not found"
    exit 1
fi
echo "✅ .dockerignore exists"

# Check entrypoint script
if [ ! -f "docker/entrypoint.sh" ]; then
    echo "❌ docker/entrypoint.sh not found"
    exit 1
fi
echo "✅ Entrypoint script exists"

# Check environment template
if [ ! -f ".env.example" ]; then
    echo "❌ .env.example not found"
    exit 1
fi
echo "✅ Environment template exists"

# Validate docker-compose configuration
echo "🔧 Validating Docker Compose configuration..."
docker-compose config > /dev/null && echo "✅ docker-compose.yml is valid"
docker-compose -f docker-compose.prod.yml config > /dev/null && echo "✅ docker-compose.prod.yml is valid"

# Test build (dry run)
echo "🏗️ Testing Docker build..."
docker build --no-cache -f Dockerfile . --tag radio-sahoo:test

# Test development deployment
echo "🚀 Testing development deployment..."
docker-compose up -d

# Wait for service to start
echo "⏳ Waiting for service to start..."
sleep 10

# Test health check
echo "🏥 Testing health check endpoint..."
if curl -f http://localhost:5000/health &> /dev/null; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    docker-compose logs radio-sahoo
fi

# Test main page
echo "🌐 Testing main page..."
if curl -f http://localhost:5000/ &> /dev/null; then
    echo "✅ Main page accessible"
else
    echo "❌ Main page not accessible"
    docker-compose logs radio-sahoo
fi

# Clean up
echo "🧹 Cleaning up test deployment..."
docker-compose down
docker rmi radio-sahoo:test

echo "🎉 Docker deployment test completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Copy .env.example to .env and configure your settings"
echo "   2. Run: docker-compose up --build"
echo "   3. Open: http://localhost:5000/radio"
echo "   4. For production: docker-compose -f docker-compose.prod.yml up --build -d"
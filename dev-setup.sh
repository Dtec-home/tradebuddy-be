#!/bin/bash

echo "🚀 Setting up TradeBuddy Development Environment (No Docker)..."

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client not found. Make sure PostgreSQL is installed and running."
fi

if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis client not found. Make sure Redis is installed and running."
fi

# Backend setup
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Created .env file. Please update it with your database credentials."
fi

# Initialize alembic if not done
if [ ! -d "alembic" ]; then
    alembic init alembic
    echo "📊 Initialized Alembic for database migrations"
fi

cd ..

# Frontend setup
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
npm install

cd ..

echo "✅ Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure PostgreSQL is running on port 5432"
echo "2. Make sure Redis is running on port 6379"
echo "3. Update backend/.env with your database credentials"
echo ""
echo "To start the backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "To start the frontend (in another terminal):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "🌐 Frontend will be at: http://localhost:3000"
echo "🔧 Backend API will be at: http://localhost:8000"
echo "📚 API Docs will be at: http://localhost:8000/docs"
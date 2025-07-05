#!/bin/bash

echo "🚀 Setting up TradeBuddy Local Development Environment..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL not found. Installing..."
    read -p "Do you want to install PostgreSQL? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        
        # Create database
        sudo -u postgres createdb tradebuddy
        sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
        echo "✅ PostgreSQL installed and database created"
    else
        echo "⚠️  You'll need to install PostgreSQL manually"
        exit 1
    fi
else
    echo "✅ PostgreSQL found"
fi

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis not found. Installing..."
    read -p "Do you want to install Redis? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install redis-server
        sudo systemctl start redis-server
        sudo systemctl enable redis-server
        echo "✅ Redis installed and started"
    else
        echo "⚠️  You'll need to install Redis manually"
        exit 1
    fi
else
    echo "✅ Redis found"
fi

# Start services
echo "🔄 Starting services..."
sudo systemctl start postgresql redis-server

# Setup backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Setup environment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Created .env file"
fi

# Initialize database
echo "📊 Setting up database..."
python test_setup.py

cd ..

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the services:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "🌐 Access points:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
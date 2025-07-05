# 🚀 TradeBuddy Quick Start Guide

## Option 1: Manual Development Setup (Recommended)

Since Docker isn't running, let's set up the development environment manually:

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Step 1: Install System Dependencies (Ubuntu/Debian)

```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server

# Start services
sudo systemctl start postgresql
sudo systemctl start redis-server

# Create database
sudo -u postgres createdb tradebuddy
```

### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Edit .env file with your database credentials:
# DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/tradebuddy
```

### Step 3: Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install
```

### Step 4: Initialize Database

```bash
cd ../backend
source venv/bin/activate

# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

### Step 5: Start Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## Option 2: Docker Setup (If Docker is Running)

### Start Docker Daemon
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Run with Docker
```bash
./start.sh
```

---

## Testing the Setup

1. **Check Backend Health**:
   ```bash
   curl http://localhost:8000/
   ```
   Should return: `{"name":"TradeBuddy","version":"1.0.0","status":"online"}`

2. **Access Frontend**: 
   Open http://localhost:3000 in your browser

3. **View API Docs**: 
   Open http://localhost:8000/docs for interactive API documentation

---

## Development Workflow

### Backend Development
- Code is in `backend/app/`
- FastAPI with auto-reload enabled
- SQLAlchemy for database ORM
- JWT authentication

### Frontend Development  
- Code is in `frontend/src/`
- Next.js with TypeScript
- Tailwind CSS + shadcn/ui components
- Real-time updates via WebSocket

### Database Changes
```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Your change description"
alembic upgrade head
```

---

## Troubleshooting

### Backend Issues
- **Port 8000 in use**: `lsof -ti:8000 | xargs kill -9`
- **Database connection**: Check PostgreSQL is running and credentials in `.env`
- **Python dependencies**: Re-run `pip install -r requirements.txt`

### Frontend Issues  
- **Port 3000 in use**: `lsof -ti:3000 | xargs kill -9`
- **Node modules**: Delete `node_modules` and run `npm install`

### Database Issues
- **Can't connect**: Check if PostgreSQL is running: `sudo systemctl status postgresql`
- **Database doesn't exist**: `sudo -u postgres createdb tradebuddy`

---

## Next Steps

1. Register a new user via the API or frontend
2. Create your first trading bot
3. Configure exchange API keys
4. Start trading!

For more detailed documentation, see `IMPLEMENTATION.md`.
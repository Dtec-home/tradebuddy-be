# Docker Troubleshooting Guide

## ✅ Issues Fixed

1. **Docker Context**: Switched from `desktop-linux` to `default`
2. **Docker Compose Version**: Removed obsolete version attribute

## 🔍 Current Issue

Docker daemon is running but containers fail with shim version error. This is a runtime compatibility issue.

## 🛠️ Solutions to Try

### Option 1: Restart Docker Service
```bash
sudo systemctl restart docker
docker run --rm hello-world
```

### Option 2: Clean Docker Installation
```bash
# Remove existing Docker completely
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt autoremove

# Install Docker Engine fresh
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Test
docker run hello-world
```

### Option 3: Fix containerd
```bash
sudo systemctl restart containerd
sudo systemctl restart docker
```

### Option 4: Use Alternative Container Runtime
```bash
# Install podman as alternative
sudo apt install podman
podman run --rm hello-world
```

## 🚀 Alternative: Manual Development Setup

If Docker continues to have issues, use the manual setup instead:

```bash
cd TradeBuddy
./dev-setup.sh
```

Then follow the manual setup instructions in `QUICK_START.md`.

## ✅ Verification Steps

After fixing Docker:
1. `docker --version` - Check version
2. `docker info` - Check daemon connection  
3. `docker run --rm hello-world` - Test container
4. `cd TradeBuddy && ./start.sh` - Start TradeBuddy

## 🔧 Quick Manual Start (No Docker)

```bash
# Terminal 1 - Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl start redis-server

# Terminal 2 - Backend
cd TradeBuddy/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
uvicorn app.main:app --reload

# Terminal 3 - Frontend  
cd TradeBuddy/frontend
npm install
npm run dev
```

Access at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
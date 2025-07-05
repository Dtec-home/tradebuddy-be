# TradeBuddy - Bot as a Service Platform

A multi-tenant cryptocurrency trading bot platform that allows users to create, deploy, and manage automated trading bots.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 14+ with TypeScript
- **UI**: shadcn/ui + Tailwind CSS
- **Database**: PostgreSQL + Redis
- **Trading Engine**: Custom Bot + Freqtrade integration
- **Container**: Docker + Kubernetes
- **Monitoring**: Prometheus + Grafana

## Project Structure

```
TradeBuddy/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docker/           # Docker configurations
├── docs/             # Documentation
└── README.md         # This file
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+

### Development Setup

1. Clone the repository
2. Set up the backend (see backend/README.md)
3. Set up the frontend (see frontend/README.md)
4. Run with Docker Compose: `docker-compose up`

## License

Proprietary - All rights reserved
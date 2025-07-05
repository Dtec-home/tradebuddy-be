# Render Deployment Guide for TradeBuddy Backend

## Quick Deploy with render.yaml

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and set up:
     - Web service (backend)
     - PostgreSQL database
     - Redis instance

## Manual Deploy (Alternative)

If you prefer manual setup:

1. **Create Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub and select your repo
   - Configure:
     - **Name**: tradebuddy-backend
     - **Root Directory**: backend
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Add PostgreSQL**
   - Click "New +" → "PostgreSQL"
   - Create database with free plan
   - Copy the connection string

3. **Add Redis**
   - Click "New +" → "Redis"
   - Create Redis instance with free plan
   - Copy the connection string

4. **Environment Variables**
   Add these in your web service settings:

   ```
   SECRET_KEY=<generate-secure-key>
   DATABASE_URL=<from-postgresql-service>
   REDIS_URL=<from-redis-service>
   BACKEND_CORS_ORIGINS=["https://tradebuddy-seven.vercel.app"]
   
   # For Celery
   CELERY_BROKER_URL=<redis-url>
   CELERY_RESULT_BACKEND=<redis-url>
   
   # OAuth (if using)
   GOOGLE_CLIENT_ID=<your-client-id>
   GOOGLE_CLIENT_SECRET=<your-client-secret>
   OAUTH_REDIRECT_URI=https://tradebuddy-seven.vercel.app/auth/callback
   
   # Bitget API
   BITGET_API_KEY=<your-api-key>
   BITGET_SECRET=<your-secret>
   BITGET_PASSPHRASE=<your-passphrase>
   BITGET_SANDBOX=false
   ```

## Post-Deployment

1. **Run Database Migrations**
   - In Render dashboard, go to your web service
   - Click "Shell" tab
   - Run: `cd backend && alembic upgrade head`

2. **Update Frontend**
   Update your frontend API URL to your Render backend URL:
   ```typescript
   // frontend/src/services/api.ts
   const API_BASE_URL = 'https://your-app.onrender.com';
   ```

## Notes

- Free tier services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- PostgreSQL free tier has 90-day retention
- Consider upgrading for production use
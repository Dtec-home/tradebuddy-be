# Railway Deployment Guide for TradeBuddy Backend

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub account
- Your TradeBuddy repository

## Deployment Steps

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Deploy on Railway

1. **Login to Railway**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your TradeBuddy repository

3. **Add PostgreSQL Database**
   - In your Railway project, click "New"
   - Select "Database" > "Add PostgreSQL"
   - Railway will automatically set DATABASE_URL

4. **Add Redis**
   - Click "New" again
   - Select "Database" > "Add Redis"
   - Note the REDIS_URL for later

5. **Configure Environment Variables**
   
   Click on your backend service and go to "Variables" tab. Add:

   ```
   # Security (IMPORTANT: Generate a secure key!)
   SECRET_KEY=<generate-a-secure-random-key>
   
   # CORS
   BACKEND_CORS_ORIGINS=["https://tradebuddy-seven.vercel.app"]
   
   # Redis (copy from your Redis service)
   REDIS_URL=<your-redis-url>
   
   # Celery (use same Redis with different databases)
   CELERY_BROKER_URL=<your-redis-url>/1
   CELERY_RESULT_BACKEND=<your-redis-url>/2
   
   # OAuth (if using Google login)
   GOOGLE_CLIENT_ID=<your-google-client-id>
   GOOGLE_CLIENT_SECRET=<your-google-client-secret>
   OAUTH_REDIRECT_URI=https://tradebuddy-seven.vercel.app/auth/callback
   
   # Bitget API (for trading)
   BITGET_API_KEY=<your-api-key>
   BITGET_SECRET=<your-secret>
   BITGET_PASSPHRASE=<your-passphrase>
   BITGET_SANDBOX=false
   ```

6. **Deploy**
   - Railway will automatically deploy your app
   - Check the deployment logs for any errors

### 3. Set Up Custom Domain (Optional)
1. In Railway, go to your backend service
2. Click on "Settings" > "Networking"
3. Generate a domain or add your custom domain

### 4. Update Frontend Configuration

Update your frontend API URL to point to your Railway backend:

```typescript
// In frontend/src/services/api.ts
const API_BASE_URL = 'https://your-app.railway.app';
```

### 5. Initialize Database

After deployment, you need to run database migrations:

1. In Railway, click on your backend service
2. Go to "Settings" > "Deploy"
3. Add a one-time command: `cd backend && alembic upgrade head`
4. Or use Railway CLI:
   ```bash
   railway run cd backend && alembic upgrade head
   ```

## Important Notes

- **DATABASE_URL**: Railway automatically injects this for PostgreSQL
- **PORT**: Railway automatically sets this, don't hardcode it
- **SSL**: Railway provides automatic SSL certificates
- **Logs**: Check deployment logs in Railway dashboard
- **Scaling**: Upgrade to paid plan for better performance

## Troubleshooting

1. **Build Failures**
   - Check your requirements.txt is complete
   - Ensure Python version compatibility

2. **Database Connection**
   - DATABASE_URL should use `postgresql+asyncpg://`
   - Check database is provisioned

3. **CORS Issues**
   - Ensure frontend URL is in BACKEND_CORS_ORIGINS
   - Include protocol (https://)

4. **Environment Variables**
   - All sensitive data should be in Railway variables
   - Never commit .env files with real credentials

## Monitoring

- View logs: Railway Dashboard > Your Service > Logs
- Check metrics: Railway Dashboard > Your Service > Metrics
- Set up alerts in Railway settings

## Next Steps

1. Test all endpoints
2. Set up monitoring/alerts
3. Configure auto-deploy from GitHub
4. Consider adding a CDN for static assets
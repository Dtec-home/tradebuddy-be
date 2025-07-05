# Google OAuth Setup for TradeBuddy

## Steps to Enable Google OAuth

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select an existing project
3. Give it a name like "TradeBuddy"

### 2. Enable Google OAuth

1. In the Google Cloud Console, go to **APIs & Services** > **OAuth consent screen**
2. Choose "External" user type
3. Fill in the required fields:
   - App name: TradeBuddy
   - User support email: Your email
   - Developer contact: Your email
4. Add scopes: `email`, `profile`, `openid`
5. Save and continue

### 3. Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose "Web application"
4. Add authorized redirect URIs:
   - `http://localhost:3000/auth/callback`
   - `http://localhost:8000/api/v1/auth/google/callback` (for development)
5. Click "Create"

### 4. Configure Your Application

1. Copy the **Client ID** and **Client Secret**
2. Update the backend `.env` file:

```env
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
OAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
```

### 5. Test the Integration

1. Start your backend: `uvicorn app.main:app --reload`
2. Start your frontend: `npm run dev`
3. Visit `http://localhost:3000`
4. Click "Get Started with Google"
5. You should be redirected to Google's login page
6. After successful login, you'll be redirected back to the dashboard

## Production Considerations

When deploying to production:

1. Update the redirect URIs in Google Cloud Console to include your production domain
2. Update the `.env` file with production URLs
3. Ensure HTTPS is enabled for production domains
4. Consider implementing refresh tokens for better user experience

## Troubleshooting

- **Error: redirect_uri_mismatch**: Make sure the redirect URI in your app matches exactly what's configured in Google Cloud Console
- **Error: invalid_client**: Double-check your client ID and secret are correct
- **CORS errors**: Ensure your backend CORS settings include your frontend URL
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.config import settings

# OAuth configuration
config = Config()
oauth = OAuth(config)

# Register Google OAuth
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def get_oauth_client():
    return oauth
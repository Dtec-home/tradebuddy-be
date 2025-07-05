from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
import string
import httpx

from app import models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.session import get_db

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await deps.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.User)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await deps.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    
    user = await deps.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists.",
        )
    
    user = await deps.create_user(db, user_in=user_in)
    return user


@router.post("/test-token", response_model=schemas.User)
async def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/test-callback")
async def test_callback(request_data: dict = Body(...)) -> Any:
    """
    Test callback endpoint to debug CORS and data format
    """
    return {
        "message": "Callback test successful",
        "received_data": request_data,
        "google_client_id": settings.GOOGLE_CLIENT_ID[:10] + "..." if settings.GOOGLE_CLIENT_ID else "NOT_SET"
    }


@router.get("/google/login")
async def google_login():
    """
    Redirect to Google OAuth login
    """
    google_oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.OAUTH_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return RedirectResponse(url=google_oauth_url)


@router.post("/google/callback")
async def google_callback(
    request_data: dict = Body(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Handle Google OAuth callback
    """
    # Extract code from request data
    code = request_data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is required")
    
    try:
        # Exchange code for token
        token_url = "https://oauth2.googleapis.com/token"
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                token_url,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.OAUTH_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }
            )
            
            if token_response.status_code != 200:
                error_detail = token_response.text()
                print(f"Token exchange failed: {error_detail}")
                raise HTTPException(status_code=400, detail=f"Failed to exchange code for token: {error_detail}")
            
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=400, detail="No access token received from Google")
            
            # Get user info
            user_info_response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_info_response.status_code != 200:
                error_detail = user_info_response.text()
                print(f"User info fetch failed: {error_detail}")
                raise HTTPException(status_code=400, detail=f"Failed to get user info: {error_detail}")
            
            user_info = user_info_response.json()
            
    except httpx.RequestError as e:
        print(f"HTTP request error: {e}")
        raise HTTPException(status_code=500, detail="Network error communicating with Google")
    except Exception as e:
        print(f"Unexpected error in OAuth flow: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during OAuth")
    
    # Check if user exists
    email = user_info.get("email")
    oauth_id = user_info.get("sub")
    
    query = select(models.User).where(models.User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        # Create new user
        username = email.split("@")[0]
        # Make sure username is unique
        base_username = username
        counter = 1
        while True:
            check_query = select(models.User).where(models.User.username == username)
            check_result = await db.execute(check_query)
            if not check_result.scalar_one_or_none():
                break
            username = f"{base_username}{counter}"
            counter += 1
        
        user = models.User(
            email=email,
            username=username,
            full_name=user_info.get("name"),
            oauth_provider="google",
            oauth_provider_id=oauth_id,
            avatar_url=user_info.get("picture"),
            is_active=True,
            is_verified=True,  # Google accounts are pre-verified
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
        }
    }
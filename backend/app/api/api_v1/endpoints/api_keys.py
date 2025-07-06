from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import ccxt

from app import models, schemas
from app.api import deps
from app.db.session import get_db
from app.schemas.api_key import (
    ApiKeyCreate, 
    ApiKeyUpdate, 
    ApiKeyResponse, 
    ApiKeyTestRequest, 
    ApiKeyTestResponse
)

router = APIRouter()


@router.post("/", response_model=ApiKeyResponse)
async def create_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_in: ApiKeyCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new exchange API key"""
    
    # Check if user already has an API key for this exchange
    query = select(models.ExchangeApiKey).where(
        and_(
            models.ExchangeApiKey.user_id == current_user.id,
            models.ExchangeApiKey.exchange == api_key_in.exchange,
            models.ExchangeApiKey.is_active == True
        )
    )
    result = await db.execute(query)
    existing_key = result.scalar_one_or_none()
    
    if existing_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Active API key for {api_key_in.exchange} already exists"
        )
    
    # Create new API key
    api_key = models.ExchangeApiKey(
        user_id=current_user.id,
        name=api_key_in.name,
        exchange=api_key_in.exchange.lower(),
        is_sandbox=api_key_in.is_sandbox,
    )
    
    # Set encrypted credentials
    api_key.set_credentials(
        api_key_in.api_key,
        api_key_in.secret,
        api_key_in.passphrase
    )
    
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    
    return ApiKeyResponse(**api_key.to_dict_safe())


@router.get("/", response_model=List[ApiKeyResponse])
async def get_api_keys(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get user's API keys"""
    
    query = select(models.ExchangeApiKey).where(
        models.ExchangeApiKey.user_id == current_user.id
    ).order_by(models.ExchangeApiKey.created_at.desc())
    
    result = await db.execute(query)
    api_keys = result.scalars().all()
    
    return [ApiKeyResponse(**key.to_dict_safe()) for key in api_keys]


@router.get("/{api_key_id}", response_model=ApiKeyResponse)
async def get_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get specific API key"""
    
    query = select(models.ExchangeApiKey).where(
        and_(
            models.ExchangeApiKey.id == api_key_id,
            models.ExchangeApiKey.user_id == current_user.id
        )
    )
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return ApiKeyResponse(**api_key.to_dict_safe())


@router.put("/{api_key_id}", response_model=ApiKeyResponse)
async def update_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_id: int,
    api_key_update: ApiKeyUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Update API key"""
    
    query = select(models.ExchangeApiKey).where(
        and_(
            models.ExchangeApiKey.id == api_key_id,
            models.ExchangeApiKey.user_id == current_user.id
        )
    )
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Update fields
    update_data = api_key_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(api_key, field, value)
    
    await db.commit()
    await db.refresh(api_key)
    
    return ApiKeyResponse(**api_key.to_dict_safe())


@router.delete("/{api_key_id}")
async def delete_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Delete API key"""
    
    query = select(models.ExchangeApiKey).where(
        and_(
            models.ExchangeApiKey.id == api_key_id,
            models.ExchangeApiKey.user_id == current_user.id
        )
    )
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Check if API key is used by any active bots
    bot_query = select(models.Bot).where(
        and_(
            models.Bot.user_id == current_user.id,
            models.Bot.exchange == api_key.exchange,
            models.Bot.status.in_(["RUNNING", "CREATED"])
        )
    )
    bot_result = await db.execute(bot_query)
    active_bots = bot_result.scalars().all()
    
    if active_bots:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete API key. {len(active_bots)} active bot(s) are using this exchange."
        )
    
    await db.delete(api_key)
    await db.commit()
    
    return {"message": "API key deleted successfully"}


@router.post("/{api_key_id}/test", response_model=ApiKeyTestResponse)
async def test_api_key(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Test API key connection"""
    
    query = select(models.ExchangeApiKey).where(
        and_(
            models.ExchangeApiKey.id == api_key_id,
            models.ExchangeApiKey.user_id == current_user.id
        )
    )
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    try:
        # Get decrypted credentials
        credentials = api_key.get_credentials()
        
        # Create exchange instance
        exchange_config = {
            'apiKey': credentials['api_key'],
            'secret': credentials['secret'],
            'sandbox': api_key.is_sandbox,
            'enableRateLimit': True,
        }
        
        # Add passphrase if provided (for exchanges like OKX, Bitget)
        if credentials.get('passphrase'):
            exchange_config['password'] = credentials['passphrase']
        
        # Initialize exchange
        if api_key.exchange == 'bitget':
            exchange = ccxt.bitget(exchange_config)
        elif api_key.exchange == 'binance':
            exchange = ccxt.binance(exchange_config)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exchange {api_key.exchange} not supported"
            )
        
        # Test connection by fetching balance
        balance = await exchange.fetch_balance()
        
        # Mark as verified
        api_key.mark_verified()
        await db.commit()
        
        # Return success response with basic balance info
        return ApiKeyTestResponse(
            success=True,
            message="API key verified successfully",
            balance_info={
                "total_balance_usd": balance.get('total', 0),
                "free_balance_usd": balance.get('free', 0),
                "used_balance_usd": balance.get('used', 0),
            }
        )
        
    except Exception as e:
        error_msg = str(e)
        return ApiKeyTestResponse(
            success=False,
            message="API key verification failed",
            error_details=error_msg
        )


@router.get("/{api_key_id}/balance")
async def get_account_balance(
    *,
    db: AsyncSession = Depends(get_db),
    api_key_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get account balance using API key"""
    
    query = select(models.ExchangeApiKey).where(
        and_(
            models.ExchangeApiKey.id == api_key_id,
            models.ExchangeApiKey.user_id == current_user.id,
            models.ExchangeApiKey.is_active == True
        )
    )
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active API key not found"
        )
    
    if not api_key.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API key must be verified before use"
        )
    
    try:
        # Get decrypted credentials
        credentials = api_key.get_credentials()
        
        # Create exchange instance (same logic as test)
        exchange_config = {
            'apiKey': credentials['api_key'],
            'secret': credentials['secret'],
            'sandbox': api_key.is_sandbox,
            'enableRateLimit': True,
        }
        
        if credentials.get('passphrase'):
            exchange_config['password'] = credentials['passphrase']
        
        if api_key.exchange == 'bitget':
            exchange = ccxt.bitget(exchange_config)
        elif api_key.exchange == 'binance':
            exchange = ccxt.binance(exchange_config)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exchange {api_key.exchange} not supported"
            )
        
        # Fetch balance
        balance = await exchange.fetch_balance()
        
        return {
            "exchange": api_key.exchange,
            "is_sandbox": api_key.is_sandbox,
            "balance": balance
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch balance: {str(e)}"
        )
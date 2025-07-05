from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models, schemas
from app.api import deps
from app.db.session import get_db
from app.core.websocket import websocket_manager

router = APIRouter()


@router.get("/", response_model=List[schemas.Bot])
async def list_bots(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve user's bots.
    """
    query = select(models.Bot).where(
        models.Bot.user_id == current_user.id
    ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    bots = result.scalars().all()
    return bots


@router.post("/", response_model=schemas.Bot)
async def create_bot(
    *,
    db: AsyncSession = Depends(get_db),
    bot_in: schemas.BotCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new bot.
    """
    # Check bot limit for user
    bot_count_query = select(models.Bot).where(
        models.Bot.user_id == current_user.id
    )
    result = await db.execute(bot_count_query)
    bot_count = len(result.scalars().all())
    
    # Check subscription limits
    max_bots = deps.get_user_bot_limit(current_user)
    if bot_count >= max_bots:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Bot limit reached. You can have maximum {max_bots} bots."
        )
    
    # Create bot
    bot = models.Bot(
        **bot_in.dict(),
        user_id=current_user.id
    )
    db.add(bot)
    
    # Create default config
    config = models.BotConfig(bot=bot)
    db.add(config)
    
    await db.commit()
    await db.refresh(bot)
    
    # Send WebSocket notification
    await websocket_manager.broadcast_bot_update(
        str(current_user.id),
        str(bot.uuid),
        "created",
        {"name": bot.name, "status": bot.status}
    )
    
    return bot


@router.get("/{bot_id}", response_model=schemas.BotDetail)
async def get_bot(
    *,
    db: AsyncSession = Depends(get_db),
    bot_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get bot by ID.
    """
    bot = await deps.get_bot_by_uuid(db, bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    if bot.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return bot


@router.post("/{bot_id}/start")
async def start_bot(
    *,
    db: AsyncSession = Depends(get_db),
    bot_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Start trading bot.
    """
    bot = await deps.get_bot_by_uuid(db, bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    if bot.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if bot.status == models.BotStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bot is already running"
        )
    
    # TODO: Start bot instance
    bot.status = models.BotStatus.RUNNING
    bot.is_active = True
    
    await db.commit()
    
    # Send WebSocket notification
    await websocket_manager.broadcast_bot_update(
        str(current_user.id),
        str(bot.uuid),
        "started",
        {"status": bot.status}
    )
    
    return {"message": "Bot started successfully"}


@router.post("/{bot_id}/stop")
async def stop_bot(
    *,
    db: AsyncSession = Depends(get_db),
    bot_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Stop trading bot.
    """
    bot = await deps.get_bot_by_uuid(db, bot_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot not found"
        )
    if bot.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if bot.status != models.BotStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bot is not running"
        )
    
    # TODO: Stop bot instance
    bot.status = models.BotStatus.STOPPED
    bot.is_active = False
    
    await db.commit()
    
    # Send WebSocket notification
    await websocket_manager.broadcast_bot_update(
        str(current_user.id),
        str(bot.uuid),
        "stopped",
        {"status": bot.status}
    )
    
    return {"message": "Bot stopped successfully"}
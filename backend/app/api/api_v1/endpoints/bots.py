from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import models, schemas
from app.api import deps
from app.db.session import get_db
from app.core.websocket import websocket_manager
from app.services.bot_manager import bot_manager

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
    
    # Start bot using bot manager
    success = await bot_manager.start_bot(db, bot)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start bot. Check your API key configuration."
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
    
    # Stop bot using bot manager
    success = await bot_manager.stop_bot(db, bot)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to stop bot"
        )
    
    return {"message": "Bot stopped successfully"}


@router.put("/{bot_id}", response_model=schemas.Bot)
async def update_bot(
    *,
    db: AsyncSession = Depends(get_db),
    bot_id: str,
    bot_update: schemas.BotUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update bot configuration.
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
    
    # Cannot update running bot
    if bot.status == models.BotStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update running bot. Stop the bot first."
        )
    
    # Update bot fields
    update_data = bot_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(bot, field):
            setattr(bot, field, value)
    
    await db.commit()
    await db.refresh(bot)
    
    # Send WebSocket notification
    await websocket_manager.broadcast_bot_update(
        str(current_user.id),
        str(bot.uuid),
        "updated",
        {"name": bot.name, "status": bot.status.value}
    )
    
    return bot


@router.delete("/{bot_id}")
async def delete_bot(
    *,
    db: AsyncSession = Depends(get_db),
    bot_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete bot.
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
    
    # Cannot delete running bot
    if bot.status == models.BotStatus.RUNNING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete running bot. Stop the bot first."
        )
    
    # Stop bot if it's running in manager (safety check)
    if bot_manager.is_bot_running(str(bot.uuid)):
        await bot_manager.stop_bot(db, bot)
    
    # Delete bot (cascade will delete config and positions)
    await db.delete(bot)
    await db.commit()
    
    # Send WebSocket notification
    await websocket_manager.broadcast_bot_update(
        str(current_user.id),
        str(bot.uuid),
        "deleted",
        {"message": "Bot deleted successfully"}
    )
    
    return {"message": "Bot deleted successfully"}


@router.get("/{bot_id}/status")
async def get_bot_status(
    *,
    db: AsyncSession = Depends(get_db),
    bot_id: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get detailed bot status including trading information.
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
    
    # Get running bot instance if available
    running_bot = bot_manager.get_running_bot(str(bot.uuid))
    
    status_info = {
        "bot_id": str(bot.uuid),
        "name": bot.name,
        "status": bot.status.value,
        "is_active": bot.is_active,
        "exchange": bot.exchange,
        "symbols": bot.symbols,
        "is_running_in_manager": running_bot is not None,
        "created_at": bot.created_at.isoformat() if bot.created_at else None,
        "updated_at": bot.updated_at.isoformat() if bot.updated_at else None,
    }
    
    # Add runtime information if bot is running
    if running_bot:
        status_info["runtime_info"] = {
            "exchange_connected": running_bot.exchange is not None,
            "trading_state": running_bot.trades,
            "is_running": running_bot.is_running,
        }
    
    return status_info
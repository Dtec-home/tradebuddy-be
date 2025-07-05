from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps
from app.db.session import get_db

router = APIRouter()


@router.get("/status")
async def get_trading_status(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get overall trading status.
    """
    return {
        "status": "operational",
        "user_id": current_user.id,
        "message": "Trading engine is operational"
    }


@router.get("/balance")
async def get_account_balance(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get account balance from exchange.
    """
    # TODO: Implement actual balance fetching
    return {
        "balance": 1000.0,
        "currency": "USDT",
        "available": 950.0,
        "used": 50.0
    }


@router.get("/positions")
async def get_active_positions(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get all active positions for user's bots.
    """
    # TODO: Implement position fetching
    return {
        "positions": [],
        "total_unrealized_pnl": 0.0,
        "total_positions": 0
    }
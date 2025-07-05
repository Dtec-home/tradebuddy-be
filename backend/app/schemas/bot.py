from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.models.bot import BotStatus, TradingMode


class BotConfigBase(BaseModel):
    leverage: int = 25
    take_profit_pct: float = 0.56
    martingale_sequence: List[float] = [0.20, 0.27, 0.36, 0.47, 0.63, 0.83, 1.08, 1.43, 1.88, 2.47, 3.25]
    max_positions: int = 2
    martingale_trigger_pct: float = 1.1
    max_drawdown_pct: float = 50.0
    daily_loss_limit: float = 10.0
    position_size_limit: float = 100.0
    telegram_enabled: bool = False
    telegram_chat_id: Optional[str] = None
    discord_enabled: bool = False
    discord_webhook: Optional[str] = None
    email_notifications: bool = True


class BotConfig(BotConfigBase):
    id: int
    bot_id: int
    
    class Config:
        from_attributes = True


class BotBase(BaseModel):
    name: str
    description: Optional[str] = None
    exchange: str = "bitget"
    symbols: List[str] = ["HYPE/USDT:USDT", "NEAR/USDT:USDT"]
    strategy_type: str = "martingale"


class BotCreate(BotBase):
    pass


class BotUpdate(BotBase):
    name: Optional[str] = None
    exchange: Optional[str] = None
    symbols: Optional[List[str]] = None


class Bot(BotBase):
    id: int
    uuid: UUID
    user_id: int
    status: BotStatus
    mode: TradingMode
    is_active: bool
    total_profit_pct: float
    total_trades: int
    winning_trades: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class BotDetail(Bot):
    config: Optional[BotConfig] = None
    
    class Config:
        from_attributes = True
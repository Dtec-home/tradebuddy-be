from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.db.base import BaseModel


class BotStatus(str, enum.Enum):
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class TradingMode(str, enum.Enum):
    LIVE = "live"
    PAPER = "paper"
    BACKTEST = "backtest"


class Bot(BaseModel):
    __tablename__ = "bots"
    
    # Identification
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # Ownership
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="bots")
    
    # Status
    status = Column(Enum(BotStatus), default=BotStatus.CREATED)
    mode = Column(Enum(TradingMode), default=TradingMode.PAPER)
    is_active = Column(Boolean, default=False)
    
    # Configuration
    exchange = Column(String, default="bitget")
    symbols = Column(JSON, default=["HYPE/USDT:USDT", "NEAR/USDT:USDT"])
    strategy_type = Column(String, default="martingale")
    
    # Performance
    total_profit_pct = Column(Float, default=0.0)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    
    # Relationships
    config = relationship("BotConfig", back_populates="bot", uselist=False, cascade="all, delete-orphan")
    positions = relationship("BotPosition", back_populates="bot", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="bot", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bot {self.name} ({self.uuid})>"


class BotConfig(BaseModel):
    __tablename__ = "bot_configs"
    
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    bot = relationship("Bot", back_populates="config")
    
    # Trading parameters
    leverage = Column(Integer, default=25)
    take_profit_pct = Column(Float, default=0.56)
    martingale_sequence = Column(JSON, default=[0.20, 0.27, 0.36, 0.47, 0.63, 0.83, 1.08, 1.43, 1.88, 2.47, 3.25])
    max_positions = Column(Integer, default=2)
    martingale_trigger_pct = Column(Float, default=1.1)
    
    # Risk management
    max_drawdown_pct = Column(Float, default=50.0)
    daily_loss_limit = Column(Float, default=10.0)
    position_size_limit = Column(Float, default=100.0)
    
    # Notifications
    telegram_enabled = Column(Boolean, default=False)
    telegram_chat_id = Column(String, nullable=True)
    discord_enabled = Column(Boolean, default=False)
    discord_webhook = Column(String, nullable=True)
    email_notifications = Column(Boolean, default=True)
    
    # Advanced settings
    custom_settings = Column(JSON, default={})


class BotPosition(BaseModel):
    __tablename__ = "bot_positions"
    
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    bot = relationship("Bot", back_populates="positions")
    
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy/sell
    is_active = Column(Boolean, default=True)
    
    # Position details
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    contracts = Column(Float, nullable=False)
    
    # Martingale tracking
    current_step = Column(Integer, default=0)
    position_levels = Column(JSON, default=[])
    martingale_trigger_prices = Column(JSON, default=[])
    
    # Performance
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)


class Trade(BaseModel):
    __tablename__ = "trades"
    
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    bot = relationship("Bot", back_populates="trades")
    
    # Trade details
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    
    # Order info
    exchange_order_id = Column(String, nullable=True)
    order_type = Column(String, default="market")
    
    # Performance
    pnl = Column(Float, default=0.0)
    pnl_pct = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
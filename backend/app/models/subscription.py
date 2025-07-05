from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class SubscriptionTierType(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionTier(BaseModel):
    __tablename__ = "subscription_tiers"
    
    name = Column(String, unique=True, nullable=False)
    tier_type = Column(Enum(SubscriptionTierType), nullable=False)
    price_monthly = Column(Float, default=0.0)
    price_yearly = Column(Float, default=0.0)
    
    # Limits
    max_bots = Column(Integer, default=1)
    max_positions_per_bot = Column(Integer, default=2)
    api_calls_per_minute = Column(Integer, default=60)
    
    # Features
    backtesting_enabled = Column(Boolean, default=False)
    strategy_marketplace = Column(Boolean, default=False)
    priority_support = Column(Boolean, default=False)
    custom_strategies = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)


class Subscription(BaseModel):
    __tablename__ = "subscriptions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="subscription")
    
    tier_id = Column(Integer, ForeignKey("subscription_tiers.id"), nullable=False)
    tier = relationship("SubscriptionTier")
    
    is_active = Column(Boolean, default=True)
    stripe_subscription_id = Column(String, nullable=True)
    
    # Billing
    current_period_start = Column(String, nullable=True)
    current_period_end = Column(String, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
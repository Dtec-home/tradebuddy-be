from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import BaseModel


class ExchangeApiKey(BaseModel):
    __tablename__ = "exchange_api_keys"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="api_keys")
    
    exchange = Column(String, nullable=False)
    name = Column(String, nullable=False)  # User-friendly name
    
    # Encrypted credentials
    api_key_encrypted = Column(String, nullable=False)
    secret_encrypted = Column(String, nullable=False)
    passphrase_encrypted = Column(String, nullable=True)
    
    is_sandbox = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # For verification
    is_verified = Column(Boolean, default=False)
    last_verified_at = Column(String, nullable=True)
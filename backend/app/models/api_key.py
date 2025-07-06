from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional

from app.db.base import BaseModel
from app.core.encryption import encryption_service


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
    
    def set_credentials(self, api_key: str, secret: str, passphrase: Optional[str] = None):
        """Set encrypted credentials"""
        encrypted = encryption_service.encrypt_api_credentials(api_key, secret, passphrase)
        self.api_key_encrypted = encrypted["api_key"]
        self.secret_encrypted = encrypted["secret"]
        self.passphrase_encrypted = encrypted["passphrase"]
    
    def get_credentials(self) -> dict:
        """Get decrypted credentials"""
        encrypted_creds = {
            "api_key": self.api_key_encrypted,
            "secret": self.secret_encrypted,
            "passphrase": self.passphrase_encrypted
        }
        return encryption_service.decrypt_api_credentials(encrypted_creds)
    
    def mark_verified(self):
        """Mark API key as verified"""
        self.is_verified = True
        self.last_verified_at = datetime.utcnow().isoformat()
    
    def to_dict_safe(self) -> dict:
        """Return safe dictionary without sensitive data"""
        return {
            "id": self.id,
            "name": self.name,
            "exchange": self.exchange,
            "is_sandbox": self.is_sandbox,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "last_verified_at": self.last_verified_at,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
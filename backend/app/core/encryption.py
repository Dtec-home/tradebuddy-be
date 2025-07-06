from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional

from app.core.config import settings


class EncryptionService:
    """Service for encrypting and decrypting sensitive data like API keys"""
    
    def __init__(self):
        self._fernet = None
    
    def _get_fernet(self) -> Fernet:
        """Get or create Fernet cipher instance"""
        if self._fernet is None:
            # Use SECRET_KEY as password for key derivation
            password = settings.SECRET_KEY.encode()
            
            # Use a fixed salt for consistent key generation
            # In production, you might want to store this salt securely
            salt = b'tradebuddy_salt_v1'
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            self._fernet = Fernet(key)
        
        return self._fernet
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt a string and return base64 encoded result"""
        if not plaintext:
            return ""
        
        fernet = self._get_fernet()
        encrypted_data = fernet.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a base64 encoded encrypted string"""
        if not encrypted_data:
            return ""
        
        try:
            fernet = self._get_fernet()
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = fernet.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
    
    def encrypt_api_credentials(self, api_key: str, secret: str, passphrase: Optional[str] = None) -> dict:
        """Encrypt API credentials and return encrypted dict"""
        return {
            "api_key": self.encrypt(api_key),
            "secret": self.encrypt(secret),
            "passphrase": self.encrypt(passphrase) if passphrase else None
        }
    
    def decrypt_api_credentials(self, encrypted_credentials: dict) -> dict:
        """Decrypt API credentials from encrypted dict"""
        return {
            "api_key": self.decrypt(encrypted_credentials["api_key"]),
            "secret": self.decrypt(encrypted_credentials["secret"]),
            "passphrase": self.decrypt(encrypted_credentials["passphrase"]) if encrypted_credentials.get("passphrase") else None
        }


# Global encryption service instance
encryption_service = EncryptionService()
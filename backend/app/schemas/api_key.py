from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ApiKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User-friendly name for the API key")
    exchange: str = Field(..., description="Exchange name (e.g., 'bitget', 'binance')")
    api_key: str = Field(..., min_length=1, description="Exchange API key")
    secret: str = Field(..., min_length=1, description="Exchange API secret")
    passphrase: Optional[str] = Field(None, description="Exchange API passphrase (if required)")
    is_sandbox: bool = Field(True, description="Whether this is a sandbox/testnet API key")


class ApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    is_sandbox: Optional[bool] = None


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    exchange: str
    is_sandbox: bool
    is_active: bool
    is_verified: bool
    last_verified_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class ApiKeyTestRequest(BaseModel):
    api_key_id: int = Field(..., description="ID of the API key to test")


class ApiKeyTestResponse(BaseModel):
    success: bool
    message: str
    balance_info: Optional[dict] = None
    error_details: Optional[str] = None
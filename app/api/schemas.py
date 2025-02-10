from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Dict
from datetime import datetime

class ClienteBase(BaseModel):
    credentials: Dict
    expiry: str

class ClienteCreate(ClienteBase):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "credentials": {"token": "abc123"},
            "expiry": "2024-12-31"
        }
    })

class ClienteUpdate(BaseModel):
    credentials: Optional[Dict] = None
    expiry: Optional[str] = None
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "credentials": {"token": "novo_token"},
            "expiry": "2025-12-31"
        }
    })

class ClienteResponse(ClienteBase):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True) 
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class ClienteBase(BaseModel):
    email: EmailStr
    credentials: Optional[Dict[str, Any]] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    expiry: Optional[str] = None

    class Config:
        from_attributes = True

class ClienteInDB(ClienteResponse):
    pass 
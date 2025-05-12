from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    TRADER = "trader"

class KycStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    firebase_uid: str
    role: Role = Role.USER
    is_active: bool = True
    balance: Optional[float] = None
    kyc_status: Optional[KycStatus] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    preferred_currency: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[Role] = None
    balance: Optional[float] = None
    kyc_status: Optional[KycStatus] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    preferred_currency: Optional[str] = None

class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    last_updated_at: datetime
    
    class Config:
        from_attributes = True

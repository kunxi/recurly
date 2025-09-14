from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""
    email: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration schema."""
    email: EmailStr
    password: str
    password_confirm: str


class TaskCreate(BaseModel):
    """Task creation schema."""
    title: str
    description: Optional[str] = None
    cadence: str
    assigned_to: int


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    cadence: Optional[str] = None
    last_completed: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskRead(BaseModel):
    """Task read schema."""
    id: int
    title: str
    description: Optional[str] = None
    cadence: str
    last_completed: Optional[datetime] = None
    assigned_to: int
    created_at: datetime
    updated_at: datetime


class TaskComplete(BaseModel):
    """Task completion schema."""
    completed_at: Optional[datetime] = None

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func

if TYPE_CHECKING:
    from .task import Task


class UserBase(SQLModel):
    """Base user model with common fields"""
    email: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    """User model for database table"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    
    # Relationship to Tasks
    tasks: list["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str = Field(min_length=8, max_length=100)


class UserRead(UserBase):
    """Model for reading user data (without password)"""
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """Model for updating user data"""
    email: Optional[str] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=100)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

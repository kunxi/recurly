from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Relationship
from sqlalchemy import Column, DateTime, func, ForeignKey


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


class TaskBase(SQLModel):
    """Base task model with common fields"""
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    cadence: str = Field(max_length=100)  # e.g., "daily", "weekly", "monthly", "custom"
    last_completed: Optional[datetime] = Field(default=None)
    assigned_to: int = Field(foreign_key="users.id")


class Task(TaskBase, table=True):
    """Task model for database table"""
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    interval: Optional[int] = Field(default=None)  # Internal field, not exposed in user schemas
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    
    # Relationship to User
    user: Optional[User] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    pass


class TaskRead(TaskBase):
    """Model for reading task data"""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Model for updating task data"""
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    cadence: Optional[str] = Field(default=None, max_length=100)
    last_completed: Optional[datetime] = None
    assigned_to: Optional[int] = None

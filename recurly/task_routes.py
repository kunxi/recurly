from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from .auth import get_current_active_user
from .database import get_session
from .models import User, Task, TaskCreate, TaskRead, TaskUpdate
from .schemas import TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema, TaskRead as TaskReadSchema, TaskComplete

router = APIRouter()


@router.post("/tasks", response_model=TaskReadSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Create a new task."""
    # Verify the assigned user exists
    assigned_user = session.get(User, task_data.assigned_to)
    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assigned user not found"
        )
    
    task = Task(
        title=task_data.title,
        description=task_data.description,
        cadence=task_data.cadence,
        assigned_to=task_data.assigned_to
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@router.get("/tasks", response_model=List[TaskReadSchema])
async def read_tasks(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """Get all tasks."""
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


@router.get("/tasks/my", response_model=List[TaskReadSchema])
async def read_my_tasks(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get tasks assigned to the current user."""
    statement = select(Task).where(Task.assigned_to == current_user.id)
    tasks = session.exec(statement).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskReadSchema)
async def read_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskReadSchema)
async def update_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Update a task."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # If updating assigned_to, verify the user exists
    if task_data.assigned_to is not None:
        assigned_user = session.get(User, task_data.assigned_to)
        if not assigned_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user not found"
            )
    
    # Update task fields
    task_dict = task_data.dict(exclude_unset=True)
    for field, value in task_dict.items():
        setattr(task, field, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@router.patch("/tasks/{task_id}/complete", response_model=TaskReadSchema)
async def complete_task(
    task_id: int,
    completion_data: TaskComplete,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Mark a task as completed."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check if user is assigned to this task
    if task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only complete tasks assigned to you"
        )
    
    # Set completion time
    task.last_completed = completion_data.completed_at or datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Delete a task."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    session.delete(task)
    session.commit()
    
    return {"message": "Task deleted successfully"}

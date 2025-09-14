from typing import Union
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from recurly.routes.auth import router as auth_router
from recurly.routes.task import router as task_router
from recurly.database import create_db_and_tables
from recurly.models.user import User
from recurly.auth import get_current_active_user

app = FastAPI(title="Recurly API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

# Include task routes
app.include_router(task_router, prefix="/api", tags=["tasks"])

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Recurly API is running!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/protected")
def read_protected_data(current_user: User = Depends(get_current_active_user)):
    """Example protected route that requires authentication."""
    return {
        "message": f"Hello {current_user.email}!",
        "user_id": current_user.id,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }
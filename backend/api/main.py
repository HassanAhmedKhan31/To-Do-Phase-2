# T-304, T-305, T-306, T-307, T-308, T-311: Secure API Completion and CORS
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional

from .database import create_db_and_tables, get_session
from .models import User, Task
from .auth import get_current_user

app = FastAPI()

# T-311: Add Vercel production URL to CORS
# The frontend URL should be an environment variable in a real-world app
origins = [
    "http://localhost:3000",
    "https://your-frontend-deployment-url.vercel.app", # TODO: Replace with your actual frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# T-205: User Sync Endpoint
@app.post("/api/users/sync", response_model=User)
async def sync_user(
    current_user: User = Depends(get_current_user),
):
    """
    Called by the frontend after a user signs in or up with Better Auth.
    Ensures a user record corresponding to the JWT's auth_id exists in our database.
    The get_current_user dependency handles creation if the user is new.
    """
    return current_user

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Returns the current authenticated user."""
    return current_user

@app.post("/api/tasks/", response_model=Task)
async def create_task(task: Task, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Creates a new task owned by the current user."""
    # Ensure the task payload doesn't try to assign a different owner
    task.owner_id = current_user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/api/tasks/", response_model=List[Task])
async def read_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Reads all tasks owned by the current user."""
    tasks = session.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks

@app.get("/api/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Reads a specific task, ensuring it's owned by the current user."""
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: Task, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Updates a task, ensuring it's owned by the current user."""
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_update.dict(exclude_unset=True)
    # Prevent changing ownership
    task_data.pop("owner_id", None)
    
    for key, value in task_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Deletes a task, ensuring it's owned by the current user."""
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return

@app.patch("/api/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Toggles the completion status of a task, ensuring it's owned by the current user."""
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
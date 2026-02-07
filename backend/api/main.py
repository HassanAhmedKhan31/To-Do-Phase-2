# T-304, T-305, T-306, T-307, T-308, T-311: Secure API Completion and CORS
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional

from .database import create_db_and_tables, get_session
from .models import User, Task
from .auth import create_access_token, get_current_user, get_password_hash, verify_password

app = FastAPI()

# T-311: Add Vercel production URL to CORS
origins = [
    "http://localhost:3000",
    "https://<your-vercel-production-url>.vercel.app",
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

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=User)
async def register(user: User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.hashed_password = get_password_hash(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/tasks/", response_model=Task)
async def create_task(task: Task, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task.owner_id = current_user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/api/tasks/", response_model=List[Task])
async def read_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks

@app.get("/api/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: Task, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.patch("/api/tasks/{task_id}", response_model=Task)
async def patch_task(
    task_id: int,
    completed: Optional[bool] = None,
    title: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if completed is not None:
        task.completed = completed
    if title is not None:
        task.title = title
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@app.patch("/api/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

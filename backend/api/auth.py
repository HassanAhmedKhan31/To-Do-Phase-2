# T-204: Implement JWT Authentication middleware.
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from dotenv import load_dotenv

from .database import engine
from .models import User

load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise RuntimeError("BETTER_AUTH_SECRET not set in .env file")

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(dict):
    """Token data is a dictionary"""
    pass

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        auth_id: str = payload.get("sub")
        if auth_id is None:
            raise credentials_exception
        token_data = TokenData(sub=auth_id)
    except JWTError:
        raise credentials_exception

    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == int(token_data["sub"]))).first()
        if user is None:
            # For this project, we will create a user if they don't exist,
            # as Better Auth is the source of truth.
            # In a real-world scenario, you might want to sync users separately.
            user = User(id=int(token_data["sub"]), email=f"user_{token_data['sub']}@example.com", hashed_password="")
            session.add(user)
            session.commit()
            session.refresh(user)

    return user
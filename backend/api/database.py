# T-203: Implement the database engine and session management.
import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # In a real app, you'd want a more robust way to handle this,
    # but for the hackathon, we'll keep it simple.
    DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

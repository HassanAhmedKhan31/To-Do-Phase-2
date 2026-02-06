# Database Schema: `users` and `tasks`

This document defines the SQL schema for the PostgreSQL database, managed via SQLModel.

## Table: `users`
Stores user information. While authentication is handled by Better Auth, this table links a user's identity within our system to their tasks.

| Column Name | Data Type        | Constraints                             | Description                                  |
|-------------|------------------|-----------------------------------------|----------------------------------------------|
| `id`        | `INTEGER`        | `PRIMARY KEY`                           | Unique identifier for the user.              |
| `email`     | `VARCHAR`        | `NOT NULL`, `UNIQUE`                    | User's email, matches the Better Auth identity. |
| `auth_id`   | `VARCHAR`        | `NOT NULL`, `UNIQUE`, `INDEX`           | The unique subject (`sub`) ID from the Better Auth JWT. |

### SQLModel (Python) Representation
```python
# T-201: Database Models
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    auth_id: str = Field(index=True, unique=True)

    tasks: List["Task"] = Relationship(back_populates="owner")
```

## Table: `tasks`
Stores the todo items created by users.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY` | Unique identifier for the task. |
| `title` | `VARCHAR` | `NOT NULL` | The content/description of the task. |
| `completed` | `BOOLEAN` | `NOT NULL`, `DEFAULT false` | The completion status of the task. |
| `owner_id` | `INTEGER` | `NOT NULL`, `FOREIGN KEY (users.id)` | Links the task to a user. |

### SQLModel (Python) Representation
```python
# T-201: Database Models
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)
    owner_id: int = Field(foreign_key="user.id")

    owner: "User" = Relationship(back_populates="tasks")
```

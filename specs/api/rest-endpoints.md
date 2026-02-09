# REST API Endpoint Definitions

This document specifies the RESTful API endpoints provided by the FastAPI backend.

**Base Path**: `/api`
**Authentication**: All endpoints listed here require a valid JWT in the `Authorization: Bearer <token>` header.

---

### User Management

*Authentication and user creation are primarily handled by Better Auth. This endpoint ensures the user exists in our local database after Better Auth authentication.*

#### `POST /api/users/sync`
- **Description**: Called by the frontend after a user signs in or up via Better Auth. It ensures a user record corresponding to the JWT's `auth_id` exists in the local database. If not, it creates one.
- **Request Body**: None (User information is derived from the JWT).
- **Response `200 OK`**: (If user already exists)
  ```json
  {
    "id": 1,
    "email": "user_1@example.com",
    "hashed_password": "..."
  }
  ```
- **Response `201 Created`**: (If new user is created)
  ```json
  {
    "id": 2,
    "email": "user_2@example.com",
    "hashed_password": "..."
  }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.

#### `GET /users/me`
- **Description**: Retrieves the currently authenticated user's information.
- **Request Body**: None.
- **Response `200 OK`**:
  ```json
  {
    "id": 1,
    "email": "user_1@example.com",
    "hashed_password": "..."
  }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.

---

### Task Management

#### `GET /api/tasks`
- **Description**: Retrieves all tasks owned by the authenticated user.
- **Request Body**: None.
- **Response `200 OK`**:
  ```json
  [
    { "id": 1, "title": "Buy milk", "description": "2% fat", "completed": false, "owner_id": 1 },
    { "id": 2, "title": "Walk the dog", "description": null, "completed": true, "owner_id": 1 }
  ]
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.

#### `POST /api/tasks`
- **Description**: Creates a new task for the authenticated user. The `owner_id` is automatically set based on the authenticated user.
- **Request Body**:
  ```json
  {
    "title": "Learn FastAPI",
    "description": "Complete tutorial on SQLModel with FastAPI"
  }
  ```
- **Response `200 OK`**:
  ```json
  { "id": 3, "title": "Learn FastAPI", "description": "Complete tutorial on SQLModel with FastAPI", "completed": false, "owner_id": 1 }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.
- **Response `422 Unprocessable Entity`**: If required fields (e.g., `title`) are missing or invalid.

#### `GET /api/tasks/{task_id}`
- **Description**: Retrieves a specific task, ensuring it's owned by the authenticated user.
- **Path Parameter**: `task_id` (integer) - The ID of the task to retrieve.
- **Request Body**: None.
- **Response `200 OK`**:
  ```json
  { "id": 1, "title": "Buy milk", "description": "2% fat", "completed": false, "owner_id": 1 }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.
- **Response `404 Not Found`**: If the `task_id` does not exist OR if the task does not belong to the authenticated user.

#### `PUT /api/tasks/{task_id}`
- **Description**: Updates an existing task owned by the authenticated user. Can update `title`, `description`, or `completed` status.
- **Path Parameter**: `task_id` (integer) - The ID of the task to update.
- **Request Body**:
  ```json
  {
    "title": "Master FastAPI",
    "description": "Apply SQLModel knowledge to a real project",
    "completed": false
  }
  ```
- **Response `200 OK`**:
  ```json
  { "id": 3, "title": "Master FastAPI", "description": "Apply SQLModel knowledge to a real project", "completed": false, "owner_id": 1 }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.
- **Response `404 Not Found`**: If the `task_id` does not exist OR if the task does not belong to the authenticated user.
- **Response `422 Unprocessable Entity`**: If provided data is invalid.

#### `DELETE /api/tasks/{task_id}`
- **Description**: Deletes a task owned by the authenticated user.
- **Path Parameter**: `task_id` (integer) - The ID of the task to delete.
- **Request Body**: None.
- **Response `204 No Content`**: On successful deletion.
- **Response `401 Unauthorized`**: If JWT is invalid or missing.
- **Response `404 Not Found`**: If the `task_id` does not exist OR if the task does not belong to the authenticated user.

#### `PATCH /api/tasks/{task_id}/toggle`
- **Description**: Toggles the completion status of a task owned by the authenticated user.
- **Path Parameter**: `task_id` (integer) - The ID of the task to toggle.
- **Request Body**: None.
- **Response `200 OK`**:
  ```json
  { "id": 1, "title": "Buy milk", "description": "2% fat", "completed": true, "owner_id": 1 }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid or missing.
- **Response `404 Not Found`**: If the `task_id` does not exist OR if the task does not belong to the authenticated user.
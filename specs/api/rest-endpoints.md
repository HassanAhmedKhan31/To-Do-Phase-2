# REST API Endpoint Definitions

This document specifies the RESTful API endpoints provided by the FastAPI backend.

**Base Path**: `/api`
**Authentication**: All endpoints listed here require a valid JWT in the `Authorization: Bearer <token>` header.

---

### User Management

*Although user creation is handled by Better Auth, we may need an endpoint to sync user info post-authentication.*

#### `POST /api/users/sync`
- **Description**: Called by the frontend after a user signs in or up. It ensures a user record corresponding to the JWT's `auth_id` exists in the local database. If not, it creates one.
- **Request Body**: None (User info is from JWT).
- **Response `200 OK`**:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "auth_id": "auth0|12345"
  }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid.

---

### Task Management

#### `GET /api/tasks`
- **Description**: Retrieves all tasks owned by the authenticated user.
- **Request Body**: None.
- **Response `200 OK`**:
  ```json
  [
    { "id": 1, "title": "Buy milk", "completed": false, "owner_id": 1 },
    { "id": 2, "title": "Walk the dog", "completed": true, "owner_id": 1 }
  ]
  ```
- **Response `401 Unauthorized`**: If JWT is invalid.

#### `POST /api/tasks`
- **Description**: Creates a new task for the authenticated user.
- **Request Body**:
  ```json
  {
    "title": "Learn FastAPI"
  }
  ```
- **Response `201 Created`**:
  ```json
  { "id": 3, "title": "Learn FastAPI", "completed": false, "owner_id": 1 }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid.
- **Response `422 Unprocessable Entity`**: If `title` is missing.

#### `PUT /api/tasks/{task_id}`
- **Description**: Updates an existing task. Can be used to update the title or completion status.
- **Path Parameter**: `task_id` (integer) - The ID of the task to update.
- **Request Body**:
  ```json
  {
    "title": "Master FastAPI",
    "completed": false
  }
  ```
- **Response `200 OK`**:
  ```json
  { "id": 3, "title": "Master FastAPI", "completed": false, "owner_id": 1 }
  ```
- **Response `401 Unauthorized`**: If JWT is invalid.
- **Response `403 Forbidden`**: If the task does not belong to the user.
- **Response `404 Not Found`**: If the `task_id` does not exist.

#### `DELETE /api/tasks/{task_id}`
- **Description**: Deletes a task owned by the authenticated user.
- **Path Parameter**: `task_id` (integer) - The ID of the task to delete.
- **Request Body**: None.
- **Response `204 No Content`**: On successful deletion.
- **Response `401 Unauthorized`**: If JWT is invalid.
- **Response `403 Forbidden`**: If the task does not belong to the user.
- **Response `404 Not Found`**: If the `task_id` does not exist.

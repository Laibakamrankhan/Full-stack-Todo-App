# API Documentation

## Overview

This document describes the available API endpoints for the Todo application. All endpoints require authentication via a JWT token in the Authorization header, except for authentication endpoints.

## Authentication

All task endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

Authentication endpoints return a JWT token that can be used for subsequent requests.

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "User Name"
}
```

**Response (200):**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "User Name",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Errors:**
- 400: Invalid input data
- 409: User already exists

#### POST /api/auth/login
Authenticate a user and return a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

**Errors:**
- 401: Invalid credentials

### Tasks

#### GET /api/tasks
Get all tasks for the authenticated user.

**Query Parameters:**
- `completed` (optional): Filter by completion status (true/false)

**Response (200):**
```json
[
  {
    "id": "task-uuid",
    "title": "Task Title",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

**Errors:**
- 401: Unauthorized

#### POST /api/tasks
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "Task Title",
  "description": "Task description",
  "completed": false
}
```

**Response (200):**
```json
{
  "id": "task-uuid",
  "title": "Task Title",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Errors:**
- 401: Unauthorized

#### GET /api/tasks/{task_id}
Get a specific task by ID.

**Path Parameters:**
- `task_id`: The ID of the task to retrieve

**Response (200):**
```json
{
  "id": "task-uuid",
  "title": "Task Title",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Errors:**
- 401: Unauthorized
- 404: Task not found

#### PUT /api/tasks/{task_id}
Update a specific task by ID.

**Path Parameters:**
- `task_id`: The ID of the task to update

**Request Body:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated task description",
  "completed": true
}
```

**Response (200):**
```json
{
  "id": "task-uuid",
  "title": "Updated Task Title",
  "description": "Updated task description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

**Errors:**
- 401: Unauthorized
- 404: Task not found

#### DELETE /api/tasks/{task_id}
Delete a specific task by ID.

**Path Parameters:**
- `task_id`: The ID of the task to delete

**Response (200):**
```json
{
  "message": "Task deleted successfully"
}
```

**Errors:**
- 401: Unauthorized
- 404: Task not found

#### PATCH /api/tasks/{task_id}/complete
Toggle the completion status of a specific task.

**Path Parameters:**
- `task_id`: The ID of the task to toggle

**Response (200):**
```json
{
  "id": "task-uuid",
  "title": "Task Title",
  "description": "Task description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

**Errors:**
- 401: Unauthorized
- 404: Task not found

## Error Responses

All error responses follow the same format:

```json
{
  "detail": "Error message"
}
```

## Common Error Codes

- 400: Bad Request - Invalid input data
- 401: Unauthorized - Missing or invalid authentication token
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Requested resource does not exist
- 500: Internal Server Error - Server-side error
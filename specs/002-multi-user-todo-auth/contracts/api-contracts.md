# API Contracts: Multi-User Todo Application

**Feature**: 002-multi-user-todo-auth
**Date**: 2026-01-02
**Version**: 1.0

## Authentication Endpoints

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
- **Request**:
  - Content-Type: application/json
  - Body: `{ "email": "string", "password": "string" }`
- **Response**:
  - 200: `{ "access_token": "string", "token_type": "bearer" }`
  - 401: `{ "error": "Invalid credentials" }`
- **Headers**: None required

### POST /api/auth/register
**Description**: Register new user account
- **Request**:
  - Content-Type: application/json
  - Body: `{ "email": "string", "password": "string", "name": "string" }`
- **Response**:
  - 201: `{ "id": "string", "email": "string", "name": "string" }`
  - 400: `{ "error": "Validation error" }`
  - 409: `{ "error": "User already exists" }`
- **Headers**: None required

## Task Management Endpoints

### GET /api/tasks
**Description**: Get all tasks for the authenticated user
- **Request**:
  - Headers: `Authorization: Bearer {token}`
- **Response**:
  - 200: `{ "tasks": [ { "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "user_id": "string", "created_at": "datetime", "updated_at": "datetime" } ] }`
  - 401: `{ "error": "Unauthorized" }`
- **Query Parameters**:
  - `completed`: Filter by completion status (true/false)
  - `limit`: Limit number of results (default: 50)
  - `offset`: Offset for pagination (default: 0)

### POST /api/tasks
**Description**: Create a new task for the authenticated user
- **Request**:
  - Headers: `Authorization: Bearer {token}`
  - Content-Type: application/json
  - Body: `{ "title": "string", "description": "string" }`
- **Response**:
  - 201: `{ "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "user_id": "string", "created_at": "datetime", "updated_at": "datetime" }`
  - 400: `{ "error": "Validation error" }`
  - 401: `{ "error": "Unauthorized" }`

### GET /api/tasks/{task_id}
**Description**: Get a specific task by ID for the authenticated user
- **Request**:
  - Headers: `Authorization: Bearer {token}`
  - Path: `task_id` (UUID string)
- **Response**:
  - 200: `{ "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "user_id": "string", "created_at": "datetime", "updated_at": "datetime" }`
  - 401: `{ "error": "Unauthorized" }`
  - 403: `{ "error": "Access denied" }`
  - 404: `{ "error": "Task not found" }`

### PUT /api/tasks/{task_id}
**Description**: Update a specific task by ID for the authenticated user
- **Request**:
  - Headers: `Authorization: Bearer {token}`
  - Path: `task_id` (UUID string)
  - Content-Type: application/json
  - Body: `{ "title": "string", "description": "string", "completed": "boolean" }`
- **Response**:
  - 200: `{ "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "user_id": "string", "created_at": "datetime", "updated_at": "datetime" }`
  - 400: `{ "error": "Validation error" }`
  - 401: `{ "error": "Unauthorized" }`
  - 403: `{ "error": "Access denied" }`
  - 404: `{ "error": "Task not found" }`

### PATCH /api/tasks/{task_id}
**Description**: Partially update a specific task by ID for the authenticated user
- **Request**:
  - Headers: `Authorization: Bearer {token}`
  - Path: `task_id` (UUID string)
  - Content-Type: application/json
  - Body: `{ "title": "string", "description": "string", "completed": "boolean" }` (any combination of fields)
- **Response**:
  - 200: `{ "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "user_id": "string", "created_at": "datetime", "updated_at": "datetime" }`
  - 400: `{ "error": "Validation error" }`
  - 401: `{ "error": "Unauthorized" }`
  - 403: `{ "error": "Access denied" }`
  - 404: `{ "error": "Task not found" }`

### DELETE /api/tasks/{task_id}
**Description**: Delete a specific task by ID for the authenticated user
- **Request**:
  - Headers: `Authorization: Bearer {token}`
  - Path: `task_id` (UUID string)
- **Response**:
  - 204: No content (success)
  - 401: `{ "error": "Unauthorized" }`
  - 403: `{ "error": "Access denied" }`
  - 404: `{ "error": "Task not found" }`

## Error Response Format

All error responses follow this format:
```json
{
  "error": "Error message",
  "error_code": "error_code_string",
  "timestamp": "ISO 8601 datetime"
}
```

## Authentication Requirements

- All task endpoints require valid JWT token in Authorization header
- Token must be verified against shared secret
- User_id must be extracted from token and validated against requested resource
- Invalid tokens return 401 Unauthorized
- Mismatched user_id returns 403 Forbidden

## Rate Limiting

- All endpoints subject to rate limiting (100 requests per minute per IP)
- Exceeding rate limit returns 429 Too Many Requests
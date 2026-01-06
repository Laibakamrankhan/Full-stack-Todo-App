# Data Model: Multi-User Todo Application

**Feature**: 002-multi-user-todo-auth
**Date**: 2026-01-02
**Status**: Complete

## Entity Definitions

### User Entity
**Description**: Represents a registered user in the system
- **Attributes**:
  - `id` (string): Unique identifier from authentication provider
  - `email` (string): User's email address for identification
  - `name` (string): User's display name
  - `created_at` (datetime): Timestamp of account creation
  - `updated_at` (datetime): Timestamp of last update

**Relationships**:
- One-to-many with Task (one user can have many tasks)

### Task Entity
**Description**: Represents a todo item created by a user
- **Attributes**:
  - `id` (UUID): Universally unique identifier for the task
  - `title` (string): Title of the task (required, max 255 chars)
  - `description` (string): Optional description of the task (nullable)
  - `completed` (boolean): Status of the task (default: false)
  - `user_id` (string): Foreign key linking to the owning user
  - `created_at` (datetime): Timestamp of task creation
  - `updated_at` (datetime): Timestamp of last update

**Validation Rules**:
- `title` must not be empty
- `user_id` must reference an existing user
- `completed` defaults to false when creating new tasks

**Relationships**:
- Many-to-one with User (many tasks belong to one user)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
- Index on `tasks.user_id` for efficient user-based queries
- Index on `tasks.completed` for filtering by completion status

## State Transitions

### Task State Transitions
- **Created**: Task is initially created with `completed = false`
- **Updated**: Task can be updated (title, description, completion status)
- **Completed**: Task completion status can be toggled to `completed = true`
- **Deleted**: Task can be permanently removed by the owner

## Data Access Patterns

### User-Specific Access
- All queries must be filtered by `user_id` to enforce data isolation
- Users can only read, update, or delete their own tasks
- Backend must verify JWT token and extract `user_id` for all operations

### Common Queries
1. Get all tasks for a user: `SELECT * FROM tasks WHERE user_id = ?`
2. Get completed tasks for a user: `SELECT * FROM tasks WHERE user_id = ? AND completed = true`
3. Get pending tasks for a user: `SELECT * FROM tasks WHERE user_id = ? AND completed = false`
4. Create new task: `INSERT INTO tasks (...) VALUES (...)`
5. Update task: `UPDATE tasks SET ... WHERE id = ? AND user_id = ?`
6. Delete task: `DELETE FROM tasks WHERE id = ? AND user_id = ?`

## Security Constraints

### Data Isolation
- All database operations must include `user_id` filter
- Cross-user access prevention through database-level constraints
- Backend validation must verify ownership before operations

### Access Control
- Read operations: Only tasks belonging to authenticated user
- Write operations: Only tasks belonging to authenticated user
- Delete operations: Only tasks belonging to authenticated user
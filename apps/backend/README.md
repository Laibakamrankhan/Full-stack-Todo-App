# Todo Backend API

This is a FastAPI-based backend for a todo application with authentication and persistence.

## Deployment on Hugging Face Spaces

This application is configured to run on Hugging Face Spaces using Docker.

### Configuration

- The application listens on port 8000
- The main application instance is available as `app` in `app.py`
- Environment variables can be configured through Hugging Face Spaces settings

### Environment Variables Required

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `BETTER_AUTH_SECRET`: Secret for Better Auth

### Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

All task endpoints require a valid JWT token in the Authorization header.
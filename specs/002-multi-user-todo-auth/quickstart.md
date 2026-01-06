# Quickstart Guide: Multi-User Todo Application

**Feature**: 002-multi-user-todo-auth
**Date**: 2026-01-02
**Status**: Complete

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm/yarn
- PostgreSQL database (or Neon Serverless PostgreSQL account)
- Better Auth account (or local authentication setup)

## Environment Setup

### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost:5432/todo_db"
   export JWT_SECRET="your-super-secret-jwt-key-here"
   export BETTER_AUTH_SECRET="your-better-auth-secret"
   ```

### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install` or `yarn install`
3. Set environment variables in `.env.local`:
   ```bash
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
   ```

## Database Setup

1. Ensure PostgreSQL is running
2. Create database if it doesn't exist: `CREATE DATABASE todo_db;`
3. Run database migrations (if using alembic): `alembic upgrade head`
4. Or run the initial setup script: `python src/main.py init_db`

## Running the Application

### Backend
1. Activate virtual environment
2. Start the FastAPI server: `uvicorn src.main:app --reload --port 8000`
3. API will be available at `http://localhost:8000`
4. Documentation available at `http://localhost:8000/docs`

### Frontend
1. Navigate to frontend directory
2. Start development server: `npm run dev` or `yarn dev`
3. Application will be available at `http://localhost:3000`

## API Testing

### Using curl
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "name": "Test User"}'

# Login to get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Create a task (replace TOKEN with actual JWT)
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "This is a test task"}'
```

### Using the Frontend
1. Visit `http://localhost:3000`
2. Register or login with your credentials
3. Create, update, and manage tasks through the UI

## Configuration Options

### Database
- Default: Neon Serverless PostgreSQL
- Connection string format: `postgresql://user:pass@host:port/dbname`
- For local development, use standard PostgreSQL installation

### Authentication
- Better Auth handles user management and JWT generation
- JWT tokens are automatically included in API requests
- Token expiration: 7 days (configurable)

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT signing (required)
- `BETTER_AUTH_SECRET`: Secret for Better Auth (required)
- `API_URL`: Backend API URL for frontend
- `DEBUG`: Enable debug mode (default: false)

## Development Commands

### Backend
- Run tests: `pytest`
- Run with coverage: `pytest --cov=src`
- Format code: `black src/ tests/`
- Check types: `mypy src/`

### Frontend
- Run tests: `npm test` or `yarn test`
- Build for production: `npm run build` or `yarn build`
- Lint code: `npm run lint` or `yarn lint`
- Format code: `npm run format` or `yarn format`

## Deployment

### Backend
1. Set production environment variables
2. Run migrations in production
3. Deploy with your preferred Python hosting (Heroku, AWS, etc.)

### Frontend
1. Build for production: `npm run build`
2. Deploy static files to hosting service (Vercel, Netlify, etc.)
3. Configure environment variables for production URLs
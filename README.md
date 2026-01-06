# Evolution_of_Todo

## Overview

This is a todo application that demonstrates a progression from a simple console-based application to a full-stack web application with persistence and authentication.

## Features

- Phase 1: Console-based todo application with in-memory storage
- Phase 2: Full-stack web application with authentication and persistence
- Phase 3: Advanced features with AI integration (Coming Soon)

## Phase 1: Console Application

The first phase includes:

- Add, list, complete, and delete todos
- In-memory storage
- Command-line interface using Typer
- Console-based UI with Rich for formatting

## Phase 2: Full-Stack Web Application

The second phase includes:

- **Backend**: FastAPI with SQLModel ORM for PostgreSQL integration
- **Frontend**: Next.js 16+ with App Router for modern React development
- **Authentication**: JWT-based authentication with Better Auth
- **Database**: Neon Serverless PostgreSQL for persistence
- **Security**: User data isolation with JWT token verification
- **UI/UX**: Responsive, creative UI with animations and modern design

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (or Neon Serverless PostgreSQL account)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd apps/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp ../../.env.example .env
   ```

   Edit the `.env` file with your database connection string and JWT secret.

6. Run the backend server:
   ```bash
   python -m src.main
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd apps/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables:
   Create a `.env.local` file with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   ```

4. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The application will be available at `http://localhost:3000`.

### Environment Variables

The application requires the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `BETTER_AUTH_SECRET`: Secret for Better Auth
- `NEXT_PUBLIC_API_URL`: Backend API URL for frontend

## API Documentation

The backend API provides the following endpoints:

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Tasks
- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

All task endpoints require a valid JWT token in the Authorization header.
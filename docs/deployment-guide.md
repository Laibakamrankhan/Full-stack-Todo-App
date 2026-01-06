# Deployment Guide

This document provides instructions for deploying the Todo application to production.

## Prerequisites

- Docker and Docker Compose installed
- A server or cloud instance with at least 2GB RAM
- Domain name configured to point to your server
- SSL certificate (recommended: Let's Encrypt)

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@db:5432/todoapp
JWT_SECRET=your-super-secret-jwt-secret-key-change-in-production
BETTER_AUTH_SECRET=your-better-auth-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
```

**Important Security Notes:**
- Use a strong, randomly generated JWT_SECRET and BETTER_AUTH_SECRET
- Never commit these values to version control
- Rotate secrets regularly in production

## Docker Compose Deployment

Create a `docker-compose.yml` file in the root of the project:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: todo-db
    environment:
      POSTGRES_DB: todoapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    container_name: todo-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/todoapp
      - JWT_SECRET=${JWT_SECRET}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile
    container_name: todo-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

volumes:
  postgres_data:
```

## Dockerfiles

### Backend Dockerfile
Create `apps/backend/Dockerfile`:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
Create `apps/frontend/Dockerfile`:

```Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
```

## Deployment Steps

1. **Prepare the environment:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd Evolution_of_Todo

   # Set up environment variables
   cp apps/backend/.env.example apps/backend/.env
   # Edit the .env file with your production values
   ```

2. **Build and start the services:**
   ```bash
   docker-compose up --build -d
   ```

3. **Run database migrations:**
   ```bash
   # Access the backend container
   docker exec -it todo-backend bash

   # Run migrations (you'll need to set up alembic properly first)
   alembic upgrade head
   ```

4. **Verify the deployment:**
   - Backend API: http://your-domain:8000/docs
   - Frontend: http://your-domain:3000

## Production Verification Checklist

- [ ] Application starts without errors
- [ ] Health checks pass
- [ ] Database connections are established
- [ ] Authentication flow works (register/login)
- [ ] Task CRUD operations work for authenticated users
- [ ] Data isolation works (users can't access other users' tasks)
- [ ] API rate limiting is in place
- [ ] SSL certificate is properly configured
- [ ] Logs are being written and rotated
- [ ] Backup procedures are in place

## Security Considerations

- Use HTTPS in production
- Implement rate limiting to prevent abuse
- Regularly update dependencies
- Monitor logs for suspicious activity
- Implement proper input validation
- Use environment variables for secrets
- Regular security audits

## Monitoring and Maintenance

- Set up log monitoring
- Configure alerts for critical errors
- Regular database backups
- Performance monitoring
- Regular security updates
- Health check endpoints

## Rollback Plan

In case of issues:
1. Keep previous versions available
2. Use Docker tags for versioning
3. Database migration rollback procedures
4. Quick switch to backup instance if needed

## Scaling Considerations

- Use a load balancer for multiple instances
- Database connection pooling
- Redis for session management (if needed)
- CDN for static assets
- Auto-scaling based on load
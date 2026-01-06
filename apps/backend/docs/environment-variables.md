# Environment Variables

This document describes all the environment variables required for the backend application.

## Required Variables

### `DATABASE_URL`
- **Description**: PostgreSQL connection string
- **Format**: `postgresql://username:password@host:port/database_name`
- **Example**: `postgresql://user:password@localhost:5432/todo_db`
- **Required**: Yes

### `JWT_SECRET`
- **Description**: Secret key used for signing and verifying JWT tokens
- **Format**: A random string of at least 32 characters
- **Example**: `my-super-secret-jwt-key-that-is-very-long-and-random`
- **Required**: Yes

### `BETTER_AUTH_SECRET`
- **Description**: Secret key for Better Auth integration
- **Format**: A random string of at least 32 characters
- **Example**: `better-auth-secret-key-for-session-management`
- **Required**: Yes

## Optional Variables

### `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Description**: Number of minutes before JWT tokens expire
- **Default**: `30`
- **Example**: `60`
- **Required**: No

### `ALGORITHM`
- **Description**: Algorithm used for JWT token encoding
- **Default**: `HS256`
- **Example**: `HS256`
- **Required**: No

## Security Guidelines

1. **Never commit secrets**: Environment variables containing secrets should never be committed to the repository
2. **Use .env files**: Store environment variables in `.env` files that are included in `.gitignore`
3. **Strong secrets**: Use randomly generated secrets with at least 32 characters
4. **Environment-specific values**: Use different values for development, staging, and production environments

## Example .env file

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET=my-super-secret-jwt-key-that-is-very-long-and-random
BETTER_AUTH_SECRET=better-auth-secret-key-for-session-management
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```
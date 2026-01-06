from fastapi import HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from jose import JWTError, jwt
from .config import settings
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Define public routes that don't require authentication
        public_routes = ["/", "/api/auth/", "/api/auth/login", "/api/auth/register", "/docs", "/redoc", "/openapi.json"]
        logger.info(f"Processing request: {request.method} {request.url.path}")

        # Skip authentication for OPTIONS requests (preflight requests) and public routes
        if request.method == "OPTIONS" or request.url.path in public_routes:
            logger.info(f"Skipping authentication for {request.method} request: {request.url.path}")
            response = await call_next(request)
            logger.info(f"Completed request: {request.method} {request.url.path}, status: {response.status_code}")
            return response

        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            logger.warning(f"Authentication failed: No authorization header in request {request.method} {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            logger.warning(f"Authentication failed: Invalid scheme {scheme} in request {request.method} {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = param
        if not token:
            logger.warning(f"Authentication failed: No token provided in request {request.method} {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not provided",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            # Decode the JWT token
            logger.info(f"Verifying JWT token for request {request.method} {request.url.path}")
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.algorithm]
            )
            user_id = payload.get("sub")
            if user_id is None:
                logger.warning(f"Token validation failed: No user ID in payload for request {request.method} {request.url.path}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Add user info to request state
            request.state.user_id = user_id
            request.state.user_role = payload.get("role", "user")
            logger.info(f"Authentication successful for user {user_id}, request {request.method} {request.url.path}")

        except JWTError as e:
            logger.error(f"JWT token validation failed for request {request.method} {request.url.path}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        logger.info(f"Completed request: {request.method} {request.url.path}, status: {response.status_code}")
        return response
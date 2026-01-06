from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
from .config import settings
import logging


logger = logging.getLogger(__name__)


# Password hashing context - using bcrypt with proper error handling
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token bearer scheme
oauth2_scheme = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    logger.info("Verifying password hash")
    result = pwd_context.verify(plain_password, hashed_password)
    logger.info(f"Password verification result: {result is not None}")
    return result


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt, with truncation if needed.
    """
    logger.info("Hashing password")
    # Truncate password to 72 characters to avoid bcrypt limitation
    truncated_password = password[:72] if len(password) > 72 else password
    hashed = pwd_context.hash(truncated_password)
    logger.info("Password hashed successfully")
    return hashed


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the given data and expiration.
    """
    logger.info(f"Creating access token for user: {data.get('sub', 'unknown')}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.algorithm)
    logger.info(f"Access token created successfully for user: {data.get('sub', 'unknown')}")
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify a JWT token and return the payload.
    """
    logger.info("Verifying JWT token")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token verification failed: no user ID in payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        logger.info(f"Token verified successfully for user: {user_id}")
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(request: Request):
    """
    Get the current user from the request's authorization header.
    """
    logger.info("Getting current user from request")
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("No authorization header found in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]
    logger.info("Verifying token from request")
    payload = verify_token(token)
    user_id = payload.get("sub")
    user_role = payload.get("role", "user")

    logger.info(f"Current user retrieved: {user_id} with role: {user_role}")
    # In a real application, you would fetch the user from the database
    # For now, we'll just return the user_id from the token
    return {"id": user_id, "role": user_role}
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlmodel import Session
from typing import Dict
from ..models.user import UserCreate, UserRead
from ..services.auth_service import AuthService
from ..core.database import get_session
from ..core.security import oauth2_scheme
import logging


router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserRead)
async def register(
    request: Request,
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user.
    """
    try:
        logger.info(f"Registration attempt for email: {user_create.email}")
        auth_service = AuthService(session)
        user = auth_service.register_user(user_create)
        logger.info(f"Successfully registered user: {user.id}")
        return user
    except ValueError as e:
        logger.warning(f"Registration failed for {user_create.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
) -> Dict[str, str]:
    """
    Authenticate user and return access token.
    """
    try:
        logger.info(f"Login attempt for email: {email}")
        auth_service = AuthService(session)
        user = auth_service.authenticate_user(email, password)

        if not user:
            logger.warning(f"Failed login attempt for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth_service.create_access_token_for_user(user)
        logger.info(f"Successfully authenticated user: {user.id}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        # Re-raise HTTP exceptions as they are already handled
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )
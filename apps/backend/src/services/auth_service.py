from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserCreate
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings
import logging


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def register_user(self, user_create: UserCreate) -> User:
        """
        Register a new user with the provided details.
        """
        logger.info(f"Registering new user with email: {user_create.email}")

        # Check if user already exists
        existing_user = self.db_session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            logger.warning(f"Registration failed: User with email {user_create.email} already exists")
            raise ValueError("User with this email already exists")

        # Create new user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )

        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)

        logger.info(f"Successfully registered user: {db_user.id}")

        return db_user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        """
        logger.info(f"Authenticating user with email: {email}")

        user = self.db_session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user:
            logger.warning(f"Authentication failed: User with email {email} not found")
            return None

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed: Invalid password for user {email}")
            return None

        logger.info(f"Successfully authenticated user: {user.id}")

        return user

    def create_access_token_for_user(self, user: User) -> str:
        """
        Create an access token for the authenticated user.
        """
        logger.info(f"Creating access token for user: {user.id}")

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        token_data = {
            "sub": user.id,
            "email": user.email,
            "name": user.name,
            "role": "user"
        }
        token = create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        logger.info(f"Access token created successfully for user: {user.id}")

        return token
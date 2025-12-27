from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from ..models.user import User
from ..models.profile import UserProfile
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not await self.verify_password(password, user.hashed_password):
            return None

        return user

    async def create_user(self, email: str, name: str, password: str,
                         profession: Optional[str] = None,
                         experience_level: Optional[str] = None,
                         technical_background: Optional[str] = None) -> User:
        """Create a new user with profile"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password
        hashed_password = await self.get_password_hash(password)

        # Create the user
        user = User(
            id=uuid.uuid4(),
            email=email,
            name=name,
            hashed_password=hashed_password,
            is_active=True
        )

        self.db_session.add(user)
        await self.db_session.flush()  # This ensures the user ID is available

        # Create user profile if any profile information is provided
        if profession or experience_level or technical_background:
            user_profile = UserProfile(
                id=uuid.uuid4(),
                user_id=user.id,
                profession=profession,
                experience_level=experience_level,
                technical_background=technical_background,
                preferences={}
            )
            self.db_session.add(user_profile)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()
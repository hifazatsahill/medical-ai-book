"""Database connection configuration for Neon Postgres with proper connection pooling."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
import os
import sys
from typing import AsyncGenerator


class DatabaseConfig:
    """Configuration class for database connection settings."""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
        self.is_migrating = self._is_migrating()

        # Neon-specific settings
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "20"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "30"))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "300"))
        self.pool_pre_ping = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"

    def _is_migrating(self) -> bool:
        """Check if we're running in a migration context."""
        return "alembic" in " ".join(sys.argv) or "alembic" in str(sys.modules)

    def get_encoded_url(self) -> str:
        """Get the properly encoded database URL for async usage."""
        if self.is_migrating:
            # Use a dummy URL for migrations to avoid connection issues
            return "postgresql+asyncpg://user:password@localhost/dbname"
        else:
            # Create encoded URL for async usage
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://")

    def get_connect_args(self) -> dict:
        """Get connection arguments for Neon Postgres."""
        if self.is_migrating:
            return {}

        connect_args = {
            "server_settings": {
                "application_name": os.getenv("APP_NAME", "ai-medical-book-app"),
                "idle_in_transaction_session_timeout": "30000",  # 30 seconds
            }
        }

        # Neon specific settings
        if os.getenv("NEON_POOL_TIMEOUT"):
            connect_args["command_timeout"] = int(os.getenv("NEON_POOL_TIMEOUT"))

        return connect_args


# Initialize configuration
db_config = DatabaseConfig()

# Create async engine with Neon-specific configuration
engine = create_async_engine(
    db_config.get_encoded_url(),
    poolclass=AsyncAdaptedQueuePool,
    pool_size=db_config.pool_size,
    max_overflow=db_config.max_overflow,
    pool_timeout=db_config.pool_timeout,
    pool_recycle=db_config.pool_recycle,
    pool_pre_ping=db_config.pool_pre_ping,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",  # Set to False in production
    connect_args=db_config.get_connect_args()
)

# Create async session maker with proper configuration
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def close_db_connection():
    """Close the database engine connection pool."""
    await engine.dispose()
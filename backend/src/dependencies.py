from sqlalchemy.ext.asyncio import AsyncSession
from .database.connection import get_async_db, AsyncSessionLocal
from fastapi import Depends
from typing import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Convenience dependency with proper typing
DatabaseDependency = Depends(get_db)
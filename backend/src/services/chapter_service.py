from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.chapter import BookChapter
from ..models.user import User
from ..models.progress import UserProgress


class BookChapterService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_chapters(self) -> List[BookChapter]:
        """Get all book chapters"""
        query = select(BookChapter).order_by(BookChapter.chapter_number)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_chapter_by_id(self, chapter_id: str) -> Optional[BookChapter]:
        """Get specific chapter by ID"""
        query = select(BookChapter).where(BookChapter.id == chapter_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_chapter_by_slug(self, slug: str) -> Optional[BookChapter]:
        """Get specific chapter by slug"""
        query = select(BookChapter).where(BookChapter.slug == slug)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def search_chapters(self, query: str) -> List[BookChapter]:
        """Search chapters by content or title"""
        search_query = select(BookChapter).where(
            BookChapter.title.contains(query) |
            BookChapter.content.contains(query)
        )
        result = await self.db_session.execute(search_query)
        return result.scalars().all()

    async def create_chapter(self, title: str, slug: str, content: str, chapter_number: int) -> BookChapter:
        """Create a new book chapter"""
        chapter = BookChapter(
            title=title,
            slug=slug,
            content=content,
            chapter_number=chapter_number
        )
        self.db_session.add(chapter)
        await self.db_session.commit()
        await self.db_session.refresh(chapter)
        return chapter

    async def update_chapter(self, chapter_id: str, **kwargs) -> Optional[BookChapter]:
        """Update a book chapter"""
        query = select(BookChapter).where(BookChapter.id == chapter_id)
        result = await self.db_session.execute(query)
        chapter = result.scalar_one_or_none()

        if not chapter:
            return None

        # Update fields
        for key, value in kwargs.items():
            if hasattr(chapter, key):
                setattr(chapter, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(chapter)
        return chapter

    async def delete_chapter(self, chapter_id: str) -> bool:
        """Delete a book chapter"""
        query = select(BookChapter).where(BookChapter.id == chapter_id)
        result = await self.db_session.execute(query)
        chapter = result.scalar_one_or_none()

        if not chapter:
            return False

        await self.db_session.delete(chapter)
        await self.db_session.commit()
        return True
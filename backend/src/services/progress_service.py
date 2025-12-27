from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.progress import UserProgress
from ..models.chapter import BookChapter
import uuid


class ProgressService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_progress(self, user_id: str, chapter_id: str) -> Optional[UserProgress]:
        """Get user progress for a specific chapter"""
        query = select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.chapter_id == chapter_id
        )
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_user_progress(self, user_id: str) -> List[UserProgress]:
        """Get all progress records for a user"""
        query = select(UserProgress).where(UserProgress.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def update_user_progress(self, user_id: str, chapter_id: str, progress_percentage: int,
                                  time_spent: Optional[int] = None, notes: Optional[str] = None,
                                  completed: Optional[bool] = None) -> UserProgress:
        """Update or create user progress for a chapter"""
        # Check if progress record already exists
        progress = await self.get_user_progress(user_id, chapter_id)

        if progress:
            # Update existing progress
            progress.progress_percentage = max(0, min(100, progress_percentage))  # Ensure percentage is 0-100
            if time_spent is not None:
                progress.time_spent = time_spent
            if notes is not None:
                progress.notes = notes
            if completed is not None:
                progress.completed = completed
            else:
                # Auto-set completed based on progress percentage
                progress.completed = (progress_percentage >= 100)
            progress.last_accessed = None  # This will be set to current time by DB
        else:
            # Create new progress record
            progress = UserProgress(
                id=uuid.uuid4(),
                user_id=user_id,
                chapter_id=chapter_id,
                progress_percentage=max(0, min(100, progress_percentage)),  # Ensure percentage is 0-100
                time_spent=time_spent,
                notes=notes,
                completed=(progress_percentage >= 100) if completed is None else completed,
                bookmarks=[]  # Initialize with empty bookmarks
            )
            self.db_session.add(progress)

        await self.db_session.commit()
        await self.db_session.refresh(progress)
        return progress

    async def add_bookmark(self, user_id: str, chapter_id: str, position: str) -> UserProgress:
        """Add a bookmark to a chapter for a user"""
        progress = await self.get_user_progress(user_id, chapter_id)

        if not progress:
            # Create progress record if it doesn't exist
            progress = UserProgress(
                id=uuid.uuid4(),
                user_id=user_id,
                chapter_id=chapter_id,
                progress_percentage=0,
                bookmarks=[position],
                completed=False
            )
            self.db_session.add(progress)
        else:
            # Add to existing bookmarks if not already there
            if position not in progress.bookmarks:
                bookmarks = progress.bookmarks or []
                bookmarks.append(position)
                progress.bookmarks = bookmarks

        await self.db_session.commit()
        await self.db_session.refresh(progress)
        return progress

    async def get_completed_chapters(self, user_id: str) -> List[str]:
        """Get list of completed chapter IDs for a user"""
        query = select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.completed == True
        )
        result = await self.db_session.execute(query)
        completed_progress = result.scalars().all()
        return [str(progress.chapter_id) for progress in completed_progress]

    async def calculate_overall_progress(self, user_id: str) -> float:
        """Calculate overall progress percentage for a user"""
        all_progress = await self.get_all_user_progress(user_id)
        if not all_progress:
            return 0.0

        total_progress = sum(p.progress_percentage for p in all_progress)
        return total_progress / len(all_progress)
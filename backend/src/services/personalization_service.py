from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.profile import UserProfile
from ..models.chapter import BookChapter


class PersonalizationService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by user ID"""
        query = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def personalize_content(self, chapter: BookChapter, user_profile: Optional[UserProfile]) -> Dict[str, Any]:
        """Personalize chapter content based on user profile"""
        original_content = chapter.content
        personalized_content = original_content  # Default to original

        if user_profile:
            # Adjust content based on user's technical background
            if user_profile.technical_background == "medical":
                # For medical professionals, include more clinical details
                # This is a simplified example - in a real app, this would be more sophisticated
                personalized_content = self._enhance_with_clinical_details(original_content)
            elif user_profile.technical_background == "software":
                # For software engineers, explain technical implementations
                personalized_content = self._enhance_with_technical_details(original_content)
            elif user_profile.technical_background == "mixed":
                # For mixed background, provide balanced content
                personalized_content = self._balance_content(original_content)

            # Adjust based on experience level
            if user_profile.experience_level == "beginner":
                # Simplify complex concepts
                personalized_content = self._simplify_content(personalized_content)
            elif user_profile.experience_level == "advanced":
                # Add more depth and complexity
                personalized_content = self._add_depth_content(personalized_content)

        return {
            "original_content": original_content,
            "personalized_content": personalized_content,
            "adaptation_notes": self._get_adaptation_notes(user_profile)
        }

    def _enhance_with_clinical_details(self, content: str) -> str:
        """Add clinical details to content for medical professionals"""
        # This is a placeholder implementation - in a real app, this would use more sophisticated text processing
        return content

    def _enhance_with_technical_details(self, content: str) -> str:
        """Add technical details to content for software professionals"""
        # This is a placeholder implementation
        return content

    def _balance_content(self, content: str) -> str:
        """Balance content for mixed backgrounds"""
        # This is a placeholder implementation
        return content

    def _simplify_content(self, content: str) -> str:
        """Simplify complex concepts"""
        # This is a placeholder implementation
        return content

    def _add_depth_content(self, content: str) -> str:
        """Add more depth and complexity"""
        # This is a placeholder implementation
        return content

    def _get_adaptation_notes(self, user_profile: Optional[UserProfile]) -> list:
        """Get notes about the personalization applied"""
        if not user_profile:
            return ["Content provided in standard format (no user profile)"]

        notes = []
        if user_profile.technical_background:
            notes.append(f"Content adapted for {user_profile.technical_background} background")
        if user_profile.experience_level:
            notes.append(f"Content adjusted for {user_profile.experience_level} experience level")
        if user_profile.profession:
            notes.append(f"Content contextualized for {user_profile.profession}")

        return notes if notes else ["Content provided in standard format"]
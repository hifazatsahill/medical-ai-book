import hashlib
import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.translation_cache import TranslationCache
import openai
import os


class TranslationService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def translate_text(self, text: str, target_language: str = "ur", source_language: str = "en") -> str:
        """Translate text to target language using OpenAI"""
        try:
            # Create a hash of the content for caching
            content_hash = hashlib.md5(f"{text}_{target_language}_{source_language}".encode()).hexdigest()

            # Check if translation exists in cache
            cached_translation = await self._get_cached_translation(content_hash)
            if cached_translation:
                # Update last accessed time
                cached_translation.last_accessed = None  # This will be updated by the DB with current time
                await self.db_session.commit()
                return cached_translation.translated_content

            # If not in cache, translate using OpenAI
            prompt = f"""
            Translate the following text to {target_language}.
            Preserve technical accuracy and context, especially for medical terminology.
            Text to translate: {text}
            """

            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )

            translated_text = response.choices[0].message.content

            # Cache the translation
            await self._cache_translation(content_hash, text, translated_text, source_language, target_language)

            return translated_text
        except Exception as e:
            print(f"Error translating text: {e}")
            return text  # Return original text if translation fails

    async def _get_cached_translation(self, content_hash: str) -> Optional[TranslationCache]:
        """Get cached translation if it exists"""
        query = select(TranslationCache).where(TranslationCache.content_hash == content_hash)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def _cache_translation(self, content_hash: str, original_content: str,
                                translated_content: str, source_language: str, target_language: str):
        """Cache a translation"""
        translation_cache = TranslationCache(
            content_hash=content_hash,
            original_content=original_content,
            translated_content=translated_content,
            source_language=source_language,
            target_language=target_language
        )
        self.db_session.add(translation_cache)
        await self.db_session.commit()

    async def translate_chapter_content(self, chapter_content: str, target_language: str = "ur") -> str:
        """Translate chapter content to target language"""
        return await self.translate_text(chapter_content, target_language)
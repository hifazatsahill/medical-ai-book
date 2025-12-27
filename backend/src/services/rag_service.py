import asyncio
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from ..models.chapter import BookChapter
from ..models.chat import ChatSession, ChatMessage
from ..config.qdrant_config import get_qdrant_client, get_collection_name
import openai
import os
from uuid import UUID


class RAGService:
    def __init__(self, db_session: AsyncSession, qdrant_client: AsyncQdrantClient = None):
        self.db_session = db_session
        self.qdrant_client = qdrant_client or get_qdrant_client()
        self.collection_name = get_collection_name()
        self.openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def create_embeddings_for_chapter(self, chapter: BookChapter) -> bool:
        """Create embeddings for a book chapter and store in Qdrant"""
        try:
            # Create embeddings using OpenAI
            response = await self.openai_client.embeddings.create(
                input=chapter.content,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding

            # Store in Qdrant
            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=str(chapter.id),
                        vector=embedding,
                        payload={
                            "chapter_id": str(chapter.id),
                            "chapter_title": chapter.title,
                            "chapter_content": chapter.content,
                            "chapter_slug": chapter.slug,
                            "chapter_number": chapter.chapter_number
                        }
                    )
                ]
            )
            return True
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return False

    async def search_similar_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content using vector similarity"""
        try:
            # Create embedding for the query
            response = await self.openai_client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            query_embedding = response.data[0].embedding

            # Search in Qdrant
            search_results = await self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            results = []
            for result in search_results:
                results.append({
                    "chapter_id": result.payload.get("chapter_id"),
                    "chapter_title": result.payload.get("chapter_title"),
                    "content_snippet": result.payload.get("chapter_content")[:500] + "...",  # First 500 chars
                    "relevance_score": result.score,
                    "chapter_slug": result.payload.get("chapter_slug"),
                    "chapter_number": result.payload.get("chapter_number")
                })

            return results
        except Exception as e:
            print(f"Error searching similar content: {e}")
            return []

    async def generate_answer(self, query: str, context_type: str = "full_book", selected_text: Optional[str] = None) -> Dict[str, Any]:
        """Generate an answer to a query using RAG"""
        try:
            # Get relevant context based on context type
            context = ""
            sources = []

            if context_type == "selected_text" and selected_text:
                # Use provided selected text as context
                context = selected_text
                sources = [{"type": "selected_text", "content": selected_text[:200]}]
            else:
                # Search across full book content
                search_results = await self.search_similar_content(query, limit=3)
                context_parts = []
                for result in search_results:
                    context_parts.append(result["content_snippet"])
                    sources.append({
                        "chapter_id": result["chapter_id"],
                        "chapter_title": result["chapter_title"],
                        "chapter_slug": result["chapter_slug"],
                        "relevance_score": result["relevance_score"]
                    })
                context = "\n\n".join(context_parts)

            # Generate response using OpenAI
            system_prompt = "You are an AI assistant for an interactive medical laboratory diagnostics book. Provide accurate, helpful answers based on the provided context. Be concise but thorough. If the context doesn't contain the answer, say so clearly."

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ]

            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )

            answer = response.choices[0].message.content
            confidence = 0.8  # Placeholder - in a real implementation, this would be calculated

            return {
                "response": answer,
                "sources": sources,
                "confidence": confidence
            }
        except Exception as e:
            print(f"Error generating answer: {e}")
            return {
                "response": "Sorry, I encountered an error processing your request.",
                "sources": [],
                "confidence": 0.0
            }

    async def create_chat_session(self, user_id: Optional[UUID] = None, session_token: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        chat_session = ChatSession(
            user_id=user_id,
            session_token=session_token
        )
        self.db_session.add(chat_session)
        await self.db_session.commit()
        await self.db_session.refresh(chat_session)
        return chat_session

    async def add_chat_message(self, session_id: UUID, role: str, content: str,
                              context_type: Optional[str] = None, selected_text: Optional[str] = None,
                              sources: Optional[List[Dict]] = None) -> ChatMessage:
        """Add a message to a chat session"""
        chat_message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            context_type=context_type,
            selected_text=selected_text,
            sources=sources or []
        )
        self.db_session.add(chat_message)
        await self.db_session.commit()
        await self.db_session.refresh(chat_message)
        return chat_message

    async def get_user_sessions(self, user_id: UUID) -> List[ChatSession]:
        """Get all chat sessions for a user"""
        query = select(ChatSession).where(ChatSession.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_session_messages(self, session_id: UUID) -> List[ChatMessage]:
        """Get all messages in a chat session"""
        query = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp.asc())
        result = await self.db_session.execute(query)
        return result.scalars().all()
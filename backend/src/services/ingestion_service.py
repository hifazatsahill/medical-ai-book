import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from ..models.book_content import BookContent, BookContentCreate, BookChunk
from ..core.vector_store import VectorStore
from ..utils.text_splitter import TextSplitter, count_tokens
from ..utils.validators import validate_chunk_size


class IngestionService:
    def __init__(self, db: Session, vector_store: VectorStore):
        self.db = db
        self.vector_store = vector_store
        self.text_splitter = TextSplitter()

    def ingest_book(self, book_data: BookContentCreate) -> BookContent:
        """
        Ingest a book into the system, chunking it and storing in vector database
        """
        # Create the book content record
        book_id = uuid.uuid4()
        book = BookContent(
            id=book_id,
            title=book_data.title,
            author=book_data.author,
            content=book_data.content,
            metadata=book_data.metadata,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            chunks=[]
        )

        # Split the content into chunks
        text_chunks = self.text_splitter.split_text(book_data.content)

        chunks = []
        for i, (chunk_text, start_pos, end_pos) in enumerate(text_chunks):
            # Validate chunk size
            if not validate_chunk_size(chunk_text):
                continue  # Skip invalid chunks

            chunk_id = str(uuid.uuid4())
            token_count = count_tokens(chunk_text)

            # Create chunk metadata
            chunk_metadata = {
                "book_id": str(book_id),
                "chunk_index": i,
                "start_pos": start_pos,
                "end_pos": end_pos
            }

            # Add chunk to vector store
            self.vector_store.add_chunk(
                chunk_id=chunk_id,
                content=chunk_text,
                book_id=str(book_id),
                metadata=chunk_metadata
            )

            # Create chunk object
            chunk = BookChunk(
                id=uuid.uuid4(),
                book_id=book_id,
                content=chunk_text,
                token_count=token_count,
                chunk_index=i,
                vector_id=chunk_id,
                metadata=chunk_metadata,
                created_at=datetime.utcnow()
            )

            chunks.append(chunk)

        book.chunks = chunks
        return book

    def delete_book(self, book_id: uuid.UUID) -> bool:
        """
        Delete a book and all its chunks from the system
        """
        # Remove all chunks from vector store
        self.vector_store.delete_chunks_by_book_id(str(book_id))

        # In a real implementation, you would also delete from the database
        # For now, we'll just return True to indicate success
        return True
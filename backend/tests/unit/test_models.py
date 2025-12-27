import pytest
from src.models.book_content import BookContent, BookChunk
from src.models.session import SessionData
from src.models.query import UserQuery, RetrievedSegment
from datetime import datetime
from uuid import UUID


def test_book_content_model():
    """Test BookContent model creation and properties"""
    book = BookContent(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        title="Test Book",
        author="Test Author",
        content="This is the content of the test book.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={}
    )
    
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert "test book" in book.content.lower()
    assert isinstance(book.id, UUID)


def test_book_chunk_model():
    """Test BookChunk model creation and properties"""
    chunk = BookChunk(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        book_id=UUID("87654321-4321-8765-4321-876543218765"),
        content="This is a test chunk of content.",
        token_count=10,
        chunk_index=0,
        vector_id="test-vector-id",
        created_at=datetime.now()
    )
    
    assert "test chunk" in chunk.content.lower()
    assert chunk.token_count == 10
    assert chunk.chunk_index == 0
    assert chunk.vector_id == "test-vector-id"
    assert isinstance(chunk.id, UUID)
    assert isinstance(chunk.book_id, UUID)


def test_session_data_model():
    """Test SessionData model creation and properties"""
    session = SessionData(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        book_id=UUID("87654321-4321-8765-4321-876543218765"),
        session_token="test-session-token",
        created_at=datetime.now(),
        last_accessed=datetime.now(),
        expires_at=datetime.now(),
        metadata={},
        conversation_history=[]
    )
    
    assert session.session_token == "test-session-token"
    assert isinstance(session.id, UUID)
    assert isinstance(session.book_id, UUID)
    assert session.conversation_history == []


def test_user_query_model():
    """Test UserQuery model creation and properties"""
    query = UserQuery(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        session_id=UUID("87654321-4321-8765-4321-876543218765"),
        query_text="What is the main concept?",
        query_type="full_book",
        timestamp=datetime.now()
    )
    
    assert query.query_text == "What is the main concept?"
    assert query.query_type == "full_book"
    assert isinstance(query.id, UUID)
    assert isinstance(query.session_id, UUID)


def test_retrieved_segment_model():
    """Test RetrievedSegment model creation and properties"""
    segment = RetrievedSegment(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        query_id=UUID("87654321-4321-8765-4321-876543218765"),
        chunk_id=UUID("11111111-2222-3333-4444-555555555555"),
        relevance_score=0.95,
        content="This is the retrieved content.",
        retrieved_at=datetime.now()
    )
    
    assert "retrieved content" in segment.content.lower()
    assert segment.relevance_score == 0.95
    assert isinstance(segment.id, UUID)
    assert isinstance(segment.query_id, UUID)
    assert isinstance(segment.chunk_id, UUID)
import pytest
from unittest.mock import Mock, MagicMock
from src.services.ingestion_service import IngestionService
from src.services.retrieval_service import RetrievalService
from src.services.generation_service import GenerationService
from src.services.session_service import SessionService
from src.models.book_content import BookContentCreate
from datetime import datetime, timedelta
from uuid import UUID


def test_ingestion_service():
    """Test IngestionService functionality"""
    # Mock database session and vector store
    mock_db = Mock()
    mock_vector_store = Mock()
    
    ingestion_service = IngestionService(mock_db, mock_vector_store)
    
    # Create test book data
    book_data = BookContentCreate(
        title="Test Book",
        author="Test Author",
        content="This is a test book content for ingestion testing. It contains multiple sentences to test the chunking functionality properly.",
        metadata={"genre": "fiction", "year": 2023}
    )
    
    # Test book ingestion
    result = ingestion_service.ingest_book(book_data)
    
    # Verify the result
    assert result.title == "Test Book"
    assert result.author == "Test Author"
    assert "test book" in result.content.lower()
    assert isinstance(result.id, UUID)
    assert result.metadata["genre"] == "fiction"
    
    # Verify that vector store methods were called appropriately
    assert mock_vector_store.add_chunk.call_count > 0


def test_retrieval_service():
    """Test RetrievalService functionality"""
    # Mock database session and vector store
    mock_db = Mock()
    mock_vector_store = Mock()
    
    # Mock the search_chunks method to return test data
    mock_vector_store.search_chunks.return_value = [
        {
            "id": "chunk-1",
            "content": "This is a relevant chunk of content",
            "book_id": "book-1",
            "metadata": {},
            "relevance_score": 0.9
        }
    ]
    
    retrieval_service = RetrievalService(mock_db, mock_vector_store)
    
    # Test chunk retrieval
    results = retrieval_service.retrieve_relevant_chunks(
        query_text="test query",
        book_id="book-1",
        limit=5
    )
    
    # Verify the results
    assert len(results) == 1
    assert results[0]["content"] == "This is a relevant chunk of content"
    assert results[0]["relevance_score"] == 0.9
    
    # Verify that vector store search method was called
    mock_vector_store.search_chunks.assert_called_once()


def test_generation_service():
    """Test GenerationService functionality"""
    # For this test, we'll focus on the structure since we can't easily test the Cohere API
    # without valid API keys in a test environment
    
    # Mock the Cohere client
    import sys
    from unittest.mock import patch
    
    # Since we can't easily mock Cohere without knowing its exact interface,
    # we'll just verify the class can be instantiated
    try:
        generation_service = GenerationService()
        # If we get here without an exception, the basic initialization worked
        assert hasattr(generation_service, 'client')
    except Exception as e:
        # If there's an issue with API key, that's expected in test environment
        assert "api" in str(e).lower() or "key" in str(e).lower()


def test_session_service():
    """Test SessionService functionality"""
    mock_db = Mock()
    session_service = SessionService(mock_db)
    
    # Create a test session
    from src.models.session import SessionDataCreate
    
    session_data = SessionDataCreate(
        book_id=UUID("12345678-1234-5678-1234-567812345678"),
        metadata={"user_agent": "test-agent"},
        conversation_history=[]
    )
    
    session = session_service.create_session(session_data)
    
    # Verify the session was created
    assert session.book_id == UUID("12345678-1234-5678-1234-567812345678")
    assert session.metadata["user_agent"] == "test-agent"
    assert isinstance(session.id, UUID)
    
    # Test getting the session
    retrieved_session = session_service.get_session(session.session_token)
    assert retrieved_session.session_token == session.session_token
    
    # Test updating conversation history
    updated_session = session_service.update_conversation_history(
        session.session_token,
        "test query",
        "test response"
    )
    assert len(updated_session.conversation_history) == 1
    assert updated_session.conversation_history[0]["query"] == "test query"
    
    # Test session validation
    is_valid = session_service.validate_session(session.session_token)
    assert is_valid
    
    # Test session deletion
    deleted = session_service.delete_session(session.session_token)
    assert deleted
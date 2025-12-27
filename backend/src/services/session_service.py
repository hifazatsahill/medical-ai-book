import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from ..models.session import SessionData, SessionDataCreate
from ..utils.validators import validate_uuid


class SessionService:
    def __init__(self, db: Session):
        self.db = db
        # In a real implementation, this would connect to a persistent store
        # For this example, we'll use an in-memory store
        self.sessions: Dict[str, SessionData] = {}

    def create_session(self, session_data: SessionDataCreate) -> SessionData:
        """
        Create a new session for a user
        """
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=30)  # 30-minute session
        
        session = SessionData(
            id=uuid.uuid4(),
            book_id=session_data.book_id,
            session_token=session_id,
            metadata=session_data.metadata,
            conversation_history=[],
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            expires_at=expires_at
        )
        
        self.sessions[session_id] = session
        return session

    def get_session(self, session_token: str) -> Optional[SessionData]:
        """
        Retrieve a session by its token
        """
        if session_token in self.sessions:
            session = self.sessions[session_token]
            # Update last accessed time
            session.last_accessed = datetime.utcnow()
            return session
        return None

    def update_conversation_history(
        self, 
        session_token: str, 
        query: str, 
        response: str
    ) -> Optional[SessionData]:
        """
        Add a query-response pair to the session's conversation history
        """
        session = self.get_session(session_token)
        if not session:
            return None
        
        # Add the new query-response to the history
        session.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Limit history to last 10 interactions to prevent memory bloat
        session.conversation_history = session.conversation_history[-10:]
        
        # Update last accessed time
        session.last_accessed = datetime.utcnow()
        
        return session

    def validate_session(self, session_token: str) -> bool:
        """
        Validate if a session is still active (not expired)
        """
        session = self.get_session(session_token)
        if not session:
            return False
        
        # Check if session has expired
        if datetime.utcnow() > session.expires_at:
            # Session has expired, remove it
            del self.sessions[session_token]
            return False
        
        return True

    def delete_session(self, session_token: str) -> bool:
        """
        Delete a session
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
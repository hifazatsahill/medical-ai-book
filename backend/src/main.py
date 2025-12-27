from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import book_router, auth_router, rag_router, user_router
from .database import close_db_connection
import os

app = FastAPI(
    title="AI Medical Laboratory Diagnostics API",
    description="API for interactive medical AI book with RAG chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(book_router, prefix="/api/book", tags=["book"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(rag_router, prefix="/api/chat", tags=["chat"])
app.include_router(user_router, prefix="/api/user", tags=["user"])

@app.get("/")
def read_root():
    return {"message": "AI Medical Laboratory Diagnostics API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Initialize database connection pool on startup."""
    print("Starting up the application...")
    # Database connection is initialized automatically when the module is imported
    # Additional startup tasks can be added here

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection pool on shutdown."""
    print("Shutting down the application...")
    await close_db_connection()
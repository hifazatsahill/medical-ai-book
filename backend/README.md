# Integrated RAG Chatbot for Interactive Book

This project implements a retrieval-augmented generation (RAG) chatbot that enables readers to ask questions about book content and receive accurate, grounded responses. The system uses Cohere for embeddings and generation, Qdrant for vector storage, and Neon Postgres for metadata. It supports both full-book queries and selected-text-only mode, with a JavaScript widget for embedding in digital books.

## Features

- Query book content using natural language
- Support for selected-text-only queries
- Embeddable in HTML/EPUB book formats
- Session management for conversation history
- Rate limiting to prevent abuse
- Grounded responses with source citations

## Tech Stack

- **Backend**: Python 3.x with FastAPI
- **Language Model**: Cohere API
- **Vector Storage**: Qdrant Cloud
- **Database**: Neon Serverless Postgres
- **Frontend Embed**: JavaScript widget

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and connection strings
   ```

## Usage

### Import a Book

First, you need to import a book into the system:

```bash
curl -X POST http://localhost:8000/v1/books/import \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-book.epub" \
  -F "title=Your Book Title" \
  -F "author=Author Name"
```

Alternatively, you can create a collection directly with text content:

```bash
curl -X POST http://localhost:8000/v1/collections \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your Book Title",
    "author": "Author Name",
    "content": "Full text content of your book..."
  }'
```

### Create a Session

Create a session for a user to interact with the chatbot:

```bash
curl -X POST http://localhost:8000/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "bookId": "your-book-id"
  }'
```

### Query the Book Content

Ask questions about the book content:

```bash
curl -X POST http://localhost:8000/v1/collections/{collectionId}/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main concepts discussed in chapter 3?",
    "sessionId": "your-session-id"
  }'
```

To query only selected text:

```bash
curl -X POST http://localhost:8000/v1/collections/{collectionId}/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this concept?",
    "sessionId": "your-session-id",
    "selectedText": "This is the specific text the user has selected..."
  }'
```

## API Endpoints

### Health Check
- `GET /health` - Check API health status

### Collections
- `POST /collections` - Create a new book collection
- `GET /collections/{collectionId}` - Get collection details
- `POST /collections/{collectionId}/query` - Query book content

### Sessions
- `POST /sessions` - Create a new session
- `GET /sessions/{sessionId}` - Get session details

### Books
- `POST /books/import` - Import book content in various formats

## Configuration

The system uses the following environment variables:

- `COHERE_API_KEY` - Your Cohere API key for embeddings and generation
- `QDRANT_URL` - URL for Qdrant vector database
- `QDRANT_API_KEY` - API key for Qdrant
- `DATABASE_URL` - Connection string for Neon Postgres database
- `DEBUG` - Set to "True" for debug mode

## Rate Limiting

The API implements per-session rate limiting (10 queries per minute by default). Exceeding this limit will result in a 429 status code.

## Error Handling

Common error responses:
- `400 Bad Request` - Invalid input parameters
- `404 Not Found` - Requested resource doesn't exist
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server-side error

## Architecture

The system follows a modular architecture with distinct layers:

- **Models**: Data structures for book content, chunks, queries, and sessions
- **Services**: Business logic for ingestion, retrieval, generation, and session management
- **API**: FastAPI routes and middleware
- **Core**: Configuration, database, and vector store utilities
- **Utils**: Helper functions for text processing and validation

## Development

To run the application in development mode:

```bash
uvicorn src.api.main:app --reload
```

To run tests:

```bash
pytest
```

## Compliance

This implementation adheres to the following constitutional principles:
1. **Grounded Truth**: All responses derive exclusively from retrieved book content
2. **Zero Hallucination**: Explicit statements when information is not in the book
3. **Context Obedience**: Selected-text queries rely only on provided text
4. **Transparency**: Responses reflect book's wording and intent
5. **Reader-Centric Clarity**: Explanations are clear and aligned with book's tone
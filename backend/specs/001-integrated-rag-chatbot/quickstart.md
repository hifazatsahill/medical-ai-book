# Quickstart Guide: Integrated RAG Chatbot for Interactive Book

This guide will help you get started with the RAG Chatbot API for interactive books.

## Prerequisites

- Python 3.x
- Cohere API key
- Qdrant Cloud access
- Neon Serverless Postgres database
- Basic knowledge of REST APIs

## Environment Setup

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

## Getting Started

### 1. Import a Book

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

### 2. Create a Session

Create a session for a user to interact with the chatbot:

```bash
curl -X POST http://localhost:8000/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "bookId": "your-book-id"
  }'
```

### 3. Query the Book Content

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
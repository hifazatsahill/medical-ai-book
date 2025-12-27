# Qwen Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in the development of the Integrated RAG Chatbot for Interactive Book project.

## Active Technologies

- Python 3.x + FastAPI, Cohere, Qdrant-client, psycopg2-binary, Pydantic, Langchain-community (001-integrated-rag-chatbot)
- Neon Serverless Postgres for metadata and sessions, Qdrant Cloud for vector embeddings (001-integrated-rag-chatbot)

## Project Context

You are working on the implementation of a retrieval-augmented generation (RAG) chatbot that enables readers to ask questions about book content and receive accurate, grounded responses. The system uses Cohere for embeddings and generation, Qdrant for vector storage, and Neon Postgres for metadata. It supports both full-book queries and selected-text-only mode, with a JavaScript widget for embedding in digital books.

## Code Structure

The project follows a web application structure with backend API and services:

```
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book_content.py          # Book content and chunk entities
│   │   ├── session.py               # Session management
│   │   └── query.py                 # Query and response entities
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ingestion_service.py     # Book content ingestion pipeline
│   │   ├── retrieval_service.py     # Vector search and retrieval logic
│   │   ├── generation_service.py    # Cohere-based response generation
│   │   └── session_service.py       # Session management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # Main FastAPI app
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── query.py             # Query endpoints
│   │   │   ├── health.py            # Health check endpoints
│   │   │   └── collections.py       # Collection management endpoints
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── rate_limit.py        # Rate limiting middleware
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration and settings
│   │   ├── database.py              # Database connection utilities
│   │   └── vector_store.py          # Qdrant integration
│   └── utils/
│       ├── __init__.py
│       ├── text_splitter.py         # Text chunking utilities
│       └── validators.py            # Input validation utilities
├── scripts/
│   ├── __init__.py
│   ├── ingest_book.py               # Book ingestion script
│   └── test_connections.py          # Connection testing script
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── contract/
│       ├── __init__.py
│       └── test_contracts.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Development Guidelines

### Core Principles

1. **Grounded Truth**: Every answer must be derived exclusively from retrieved book content. The system shall not generate responses based on model training data or external knowledge sources when answering questions about the book.

2. **Zero Hallucination**: If information is not present in the retrieved context, the system must explicitly state that the answer is not available in the book. The system shall never fabricate, infer, or speculate beyond the provided content.

3. **Context Obedience**: When user provides selected text, answers must rely ONLY on that selected text. The system must prioritize the provided context over any other retrieved content when responding to queries.

4. **Transparency**: Answers should clearly reflect the book's wording and intent. The system shall maintain fidelity to the original text and avoid rewording in ways that might alter meaning.

5. **Reader-Centric Clarity**: Explanations should be clear, concise, and aligned with the book's level and tone. The system shall prioritize understanding and comprehension for the reader.

### Technology Constraints

- Language Model: Cohere LLM only (no OpenAI or other providers)
- Retrieval Engine: Vector-based retrieval via Qdrant
- Memory Storage: Neon Serverless Postgres for sessions and chat history
- Backend Framework: FastAPI
- Agent Orchestration: Specifikit + Qwen CLI compatible

### Implementation Requirements

- Always retrieve relevant chunks before generating an answer
- Never answer from prior knowledge or model training
- If multiple chunks conflict, prefer the most contextually relevant and recent section of the book
- Do not infer beyond the retrieved text
- Use only the provided context block
- Do not add examples, facts, or explanations not present in the book
- If the answer is missing or incomplete in the text, respond with: "This information is not available in the provided book content."
- Do not speculate
- Do not generalize

### Project-Specific Guidelines

- Implement per-session rate limiting (e.g., 10 queries per minute)
- Support importing book content in multiple formats including EPUB, MOBI, DOCX
- Chunk book content into 512-1024 token segments during preprocessing
- Provide responsive UI that works across different device sizes
- Implement proper CORS and API authentication for security
- Maintain traceability between responses and source book content
- Support querying either the entire book or user-selected text snippets
- Ensure 99.5% uptime with graceful degradation when external services fail

## Recent Changes

- 001-integrated-rag-chatbot: Added Python 3.x + FastAPI, Cohere, Qdrant-client, psycopg2-binary, Pydantic, Langchain-community
- 001-integrated-rag-chatbot: Added Neon Serverless Postgres for metadata and sessions, Qdrant Cloud for vector embeddings

**Last updated**: 2025-12-23
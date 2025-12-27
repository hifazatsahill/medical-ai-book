# Implementation Plan: Integrated RAG Chatbot for Interactive Book

**Branch**: `001-integrated-rag-chatbot` | **Date**: 2025-12-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

Implementation of a retrieval-augmented generation (RAG) chatbot that enables readers to ask questions about book content and receive accurate, grounded responses. The system will use Cohere for embeddings and generation, Qdrant for vector storage, and Neon Postgres for metadata and session management. It will support both full-book queries and selected-text-only mode, with a JavaScript widget for embedding in digital books.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: FastAPI, Cohere, Qdrant-client, psycopg2-binary, Pydantic, Langchain-community
**Storage**: Neon Serverless Postgres for metadata and sessions, Qdrant Cloud for vector embeddings
**Testing**: pytest
**Target Platform**: Linux server (backend API)
**Project Type**: Web application (backend API with JavaScript widget)
**Performance Goals**: 99.5% uptime with <3 second response time for 90% of queries
**Constraints**: <200ms p95 for internal operations, responses must be grounded in book content with zero hallucination
**Scale/Scope**: Support for 10k books, 1M+ content chunks, 1k concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All requirements from the constitution have been verified and are consistent with the project goals.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
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

**Structure Decision**: Web application structure with backend API has been selected. The backend will handle all RAG functionality and provide API endpoints for the JavaScript widget to interact with.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple external services | Need Cohere for LLM, Qdrant for vectors, Neon for metadata | Single service approach insufficient for RAG requirements |
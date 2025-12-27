# Implementation Plan: Integrated RAG Chatbot for Interactive Book

**Branch**: `001-integrated-rag-chatbot` | **Date**: 2025-12-23 | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The implementation will create a retrieval-augmented generation (RAG) chatbot that enables readers to ask questions about book content and receive accurate, grounded responses. The system will use Cohere for embeddings and generation, Qdrant for vector storage, and Neon Postgres for metadata. It will support both full-book queries and selected-text-only mode, with a JavaScript widget for embedding in digital books.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: FastAPI, Cohere, Qdrant-client, psycopg2-binary, Pydantic, Langchain-community
**Storage**: Neon Serverless Postgres for metadata and sessions, Qdrant Cloud for vector embeddings
**Testing**: Pytest for unit and integration tests
**Target Platform**: Linux server (deployable on free tier platforms like Render, Fly.io, or Railway)
**Project Type**: Web application with backend API and frontend embed widget
**Performance Goals**: <5s response time for 90% of requests, support 10 concurrent users
**Constraints**: Free-tier services only, no user data persistence beyond sessions, rate limiting at 10 queries per minute per session
**Scale/Scope**: Single book support, up to 1GB of vector storage in Qdrant

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation must adhere to the following constitutional principles:
- **Grounded Truth**: All responses must derive exclusively from retrieved book content
- **Zero Hallucination**: System must explicitly state when information is not in the book
- **Context Obedience**: Selected-text queries must rely ONLY on provided text
- **Transparency**: Responses must reflect book's wording and intent
- **Reader-Centric Clarity**: Explanations must be clear and aligned with book's tone

Technology stack compliance:
- ✅ Cohere LLM only (no OpenAI or other providers)
- ✅ Vector-based retrieval via Qdrant
- ✅ Neon Serverless Postgres for sessions and chat history
- ✅ FastAPI backend framework
- ✅ Specifikit + Qwen CLI compatible

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

**Structure Decision**: Web application structure selected with separate backend for API and services, with frontend embed widget to be developed separately. Backend contains models, services, API routes, core utilities, and scripts for ingestion. Tests are organized by type (unit, integration, contract).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
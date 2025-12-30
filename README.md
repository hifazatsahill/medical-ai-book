# AI in Medical Laboratory Diagnostics: Revolutionizing Precision and Efficiency

This repository contains the interactive digital book project titled **AI in Medical Laboratory Diagnostics: Revolutionizing Precision and Efficiency**. This project combines cutting-edge AI technologies with medical laboratory science to create an educational resource that demonstrates how artificial intelligence is transforming diagnostic medicine.

## Project Overview

The project aims to create a fully interactive digital book with:
- Comprehensive content on AI applications in medical laboratory diagnostics
- Embedded Retrieval-Augmented Generation (RAG) chatbot for intelligent Q&A
- Personalization features based on user background
- Urdu translation capabilities
- User authentication and profile management

## Architecture

The project follows a modern web application architecture with:
- **Frontend**: Next.js/React responsive web interface
- **Backend**: FastAPI server handling business logic and API endpoints
- **Database**: Neon Serverless Postgres for user data and book metadata
- **Vector Store**: Qdrant Cloud for embedding storage and similarity search
- **Authentication**: Better-Auth for user management
- **AI Services**: OpenAI Agents/ChatKit SDKs for RAG functionality

## Setup Instructions

### Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Git
- Access to OpenAI API (with sufficient quota for development)
- Neon Serverless PostgreSQL account
- Qdrant Cloud account (Free Tier)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
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

4. Create environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your credentials.

5. Run the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.local.example .env.local
   ```
   Edit `.env.local` with your API URLs.

4. Run the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## Features

### Base Requirements (100 points)
- Interactive digital book using AI/spec-driven methods
- RAG chatbot using OpenAI Agents/ChatKit SDKs, FastAPI backend, Neon Serverless Postgres, Qdrant Cloud Free Tier
- Context-aware question answering from full book or user-selected text

### Bonus Features (up to 200 points)
- **+50 points**: Reusable intelligence via Claude Code Subagents and Agent Skills
- **+50 points**: User authentication with background collection (Better-Auth)
- **+50 points**: Personalized content adaptation based on user profile
- **+50 points**: Urdu translation capabilities for all content

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Book Content
- `GET /api/book/chapters` - Get all chapters
- `GET /api/book/chapters/{slug}` - Get specific chapter
- `GET /api/book/search` - Search across book content

### RAG Chatbot
- `POST /api/chat/query` - Submit query to RAG system
- `POST /api/chat/query-selected` - Query with selected text context
- `GET /api/chat/sessions` - Get user's chat sessions
- `GET /api/chat/session/{id}/messages` - Get messages in a session

### Personalization
- `POST /api/user/personalize/chapter` - Get personalized chapter content
- `POST /api/user/translate/chapter` - Get translated chapter content

## Project Structure

```
├── backend/                 # FastAPI backend application
│   ├── src/
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── api/            # API routers
│   │   ├── database.py     # Database configuration
│   │   └── config.py       # Application configuration
│   ├── requirements.txt    # Python dependencies
│   └── setup.py           # Package configuration
├── frontend/               # Next.js frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── services/       # API services
│   │   └── styles/         # CSS styles
│   ├── package.json       # Node.js dependencies
│   └── next.config.js     # Next.js configuration
├── specs/                 # Project specifications
│   └── medical-ai-book/   # Medical AI book specifications
├── history/               # Prompt History Records
└── README.md             # This file
```

## Development

### Running Tests

**Backend Tests:**
```bash
cd backend
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## Contributing

This project follows strict quality standards for medical content accuracy. All contributions must:
- Reference primary peer-reviewed sources
- Maintain >90% relevance and factual accuracy for RAG responses
- Follow security best practices
- Support cross-browser compatibility

## Deployment

### Vercel Deployment

Both frontend and backend can be deployed on Vercel:

1. **Backend Deployment**:
   - Navigate to the `backend` directory
   - The `vercel.json` file configures the backend as a Python serverless function
   - Set the required environment variables in the Vercel dashboard:
     - `COHERE_API_KEY`
     - `QDRANT_URL`
     - `QDRANT_API_KEY`
     - `DATABASE_URL`
     - `DEBUG`

2. **Frontend Deployment**:
   - Navigate to the `frontend` directory
   - The `vercel.json` file configures the Next.js frontend
   - Set the required environment variables in the Vercel dashboard:
     - `NEXT_PUBLIC_API_BASE_URL`: URL of your deployed backend
     - `NEXT_PUBLIC_FRONTEND_URL`: URL of your deployed frontend

For detailed deployment instructions, see the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) file.

## License

This project is designed for educational purposes in medical diagnostics. Content is not a substitute for professional medical advice.
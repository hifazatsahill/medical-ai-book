# Quickstart Guide: AI in Medical Laboratory Diagnostics – Interactive Book Development

## Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Git
- Access to OpenAI API (with sufficient quota for development)
- Neon Serverless PostgreSQL account
- Qdrant Cloud account (Free Tier)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart pydantic sqlalchemy asyncpg databases python-jose[cryptography] passlib[bcrypt] openai qdrant-client python-dotenv better-auth

# Create environment file
cp .env.example .env
```

Edit `.env` with your credentials:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-api-key
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
BETTER_AUTH_SECRET=your-better-auth-secret
```

### 3. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install next react react-dom @types/react @types/node
npm install axios
npm install better-auth

# Create environment file
cp .env.example .env.local
```

Edit `.env.local` with your API URLs:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000
```

### 4. Database Setup

Run the following to initialize the database:

```bash
cd backend
python -c "
import asyncio
from src.models import create_tables
asyncio.run(create_tables())
"
```

### 5. Running the Applications

**Backend (FastAPI):**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Frontend (Next.js):**
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

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
- `POST /api/personalize/chapter` - Get personalized chapter content
- `POST /api/translate/chapter` - Get translated chapter content

## Environment Configuration

### Required Environment Variables

**Backend (.env):**
- `DATABASE_URL` - Neon PostgreSQL connection string
- `QDRANT_URL` - Qdrant Cloud cluster URL
- `QDRANT_API_KEY` - Qdrant API key
- `OPENAI_API_KEY` - OpenAI API key
- `SECRET_KEY` - JWT secret key
- `BETTER_AUTH_SECRET` - Better-Auth secret

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_FRONTEND_URL` - Frontend URL

## Development Workflow

1. **Content Development**: Add/edit book chapters in the database
2. **RAG Ingestion**: Run ingestion script to vectorize new content
3. **Testing**: Run tests to ensure functionality and accuracy
4. **Personalization**: Test content adaptation based on user profiles
5. **Translation**: Verify Urdu translation functionality

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

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Docker/Cloud)
1. Build Docker image: `docker build -t medical-ai-book .`
2. Push to container registry
3. Deploy to cloud provider (AWS, GCP, Azure)

## Troubleshooting

### Common Issues

**Qdrant Connection**: Verify API key and URL in environment variables
**OpenAI API**: Check quota and API key validity
**Database Connection**: Confirm Neon PostgreSQL connection string
**Authentication**: Ensure Better-Auth secrets are properly configured

### Performance Optimization

- Use translation caching to reduce API calls
- Implement proper indexing for database queries
- Optimize vector search parameters in Qdrant
- Implement proper caching for frequently accessed content
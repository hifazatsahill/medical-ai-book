# Deployment Guide: Frontend and Backend on Vercel

This guide explains how to deploy both the frontend (Next.js) and backend (FastAPI) applications on Vercel.

## Architecture Overview

- **Frontend**: Next.js application deployed on Vercel with static export
- **Backend**: FastAPI application adapted for Vercel serverless functions

## Prerequisites

1. Vercel account
2. Git repository for both frontend and backend code
3. Environment variables for all services (Cohere, Qdrant, Database, etc.)

## Backend Deployment on Vercel

### 1. Vercel Configuration
The backend includes a `vercel.json` file that configures it as a Python serverless function:
- All requests are routed through `api/index.py`
- The handler translates Vercel's serverless function format to FastAPI's ASGI format

### 2. Environment Variables
Set these environment variables in your Vercel project dashboard:
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant vector database URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `DATABASE_URL`: Your PostgreSQL database connection string
- `DEBUG`: Set to "True" for development, "False" for production

### 3. Deployment Steps
1. Link your backend repository to Vercel
2. Set the root directory to the `backend` folder
3. Add the environment variables listed above
4. Deploy the project

## Frontend Deployment on Vercel

### 1. Vercel Configuration
The frontend includes a `vercel.json` file that configures it as a Next.js application:
- Uses static export for better performance
- Rewrites API requests to the deployed backend

### 2. Environment Variables
Set these environment variables in your Vercel project dashboard:
- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend (e.g., `https://your-backend-deployment.vercel.app`)
- `NEXT_PUBLIC_FRONTEND_URL`: The URL of your deployed frontend (e.g., `https://your-frontend-deployment.vercel.app`)

### 3. Deployment Steps
1. Link your frontend repository to Vercel
2. Set the root directory to the `frontend` folder
3. Add the environment variables listed above
4. Deploy the project

## API Request Flow

1. Frontend makes requests to `/api/*` routes
2. Vercel's rewrite rules forward these to the backend URL
3. Backend processes the request and returns the response
4. Response is returned to the frontend

## Important Notes

1. **Database Connections**: Serverless functions have limited execution time. Ensure your database connections are optimized for short-lived requests.

2. **Cold Starts**: First requests to serverless functions may be slower due to cold starts. Consider using Vercel's warming mechanisms if needed.

3. **Rate Limits**: Be aware of Vercel's rate limits for serverless functions.

4. **Environment Variables**: Never commit secrets to version control. Always use environment variables in Vercel dashboard.

## Troubleshooting

### Common Issues:

1. **CORS Errors**: The backend API includes CORS headers, but ensure your frontend URL is properly configured.

2. **Database Connection Issues**: Verify your DATABASE_URL is correctly formatted and accessible from Vercel.

3. **API Keys**: Ensure all required API keys (Cohere, Qdrant) are properly set in environment variables.

### Debugging:

1. Check Vercel logs in your dashboard for error messages
2. Verify environment variables are correctly set
3. Test API endpoints directly using tools like curl or Postman

## Performance Considerations

1. **Optimize Dependencies**: The serverless function bundles all dependencies, so keep requirements minimal
2. **Database Connection Pooling**: Consider connection pooling strategies for better performance
3. **Caching**: Implement appropriate caching strategies for frequently accessed data
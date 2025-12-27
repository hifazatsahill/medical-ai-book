from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from uuid import UUID
import logging
from .config import settings


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Using HTTP for better compatibility
        )
        self.collection_name = "book_chunks"
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            )
            logging.info(f"Created collection: {self.collection_name}")
    
    def add_chunk(self, chunk_id: str, content: str, book_id: str, metadata: Dict[str, Any] = None):
        """Add a text chunk to the vector store"""
        if metadata is None:
            metadata = {}
        
        # In a real implementation, we would generate embeddings using Cohere
        # For now, we'll use placeholder embeddings
        embeddings = [0.0] * 1024  # Placeholder for actual embedding
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=chunk_id,
                    vector=embeddings,
                    payload={
                        "content": content,
                        "book_id": book_id,
                        "metadata": metadata
                    }
                )
            ]
        )
    
    def search_chunks(self, query_vector: List[float], book_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant chunks in the vector store for a specific book"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="book_id",
                        match=models.MatchValue(value=book_id)
                    )
                ]
            ),
            limit=limit
        )
        
        return [
            {
                "id": result.id,
                "content": result.payload["content"],
                "book_id": result.payload["book_id"],
                "metadata": result.payload["metadata"],
                "relevance_score": result.score
            }
            for result in results
        ]
    
    def delete_chunks_by_book_id(self, book_id: str):
        """Delete all chunks associated with a specific book"""
        # Find all points with the given book_id
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="book_id",
                        match=models.MatchValue(value=book_id)
                    )
                ]
            ),
            limit=10000  # Assuming no book has more than 10k chunks
        )
        
        # Extract point IDs
        point_ids = [point.id for point in results[0]]
        
        # Delete the points
        if point_ids:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=point_ids)
            )
    
    def get_chunk(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific chunk by ID"""
        results = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[chunk_id]
        )
        
        if results:
            point = results[0]
            return {
                "id": point.id,
                "content": point.payload["content"],
                "book_id": point.payload["book_id"],
                "metadata": point.payload["metadata"]
            }
        
        return None
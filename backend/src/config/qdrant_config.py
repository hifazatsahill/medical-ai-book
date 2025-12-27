"""Qdrant Cloud configuration and client setup."""
import os
from qdrant_client import AsyncQdrantClient


class QdrantConfig:
    """Configuration class for Qdrant Cloud connection."""

    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_chapters")
        self.qdrant_cloud = os.getenv("QDRANT_CLOUD", "false").lower() == "true"

    def get_client(self) -> AsyncQdrantClient:
        """Get configured Qdrant client instance."""
        if self.qdrant_cloud and self.qdrant_api_key:
            # Qdrant Cloud configuration with secure connection
            return AsyncQdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                prefer_grpc=True,  # Use gRPC for better performance
            )
        else:
            # Local Qdrant configuration
            return AsyncQdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
            )

    def get_collection_name(self) -> str:
        """Get the configured collection name."""
        return self.qdrant_collection_name

    def validate_config(self) -> bool:
        """Validate that the Qdrant configuration is complete."""
        if self.qdrant_cloud:
            return bool(self.qdrant_url and self.qdrant_api_key)
        else:
            return bool(self.qdrant_url)


# Global Qdrant configuration instance
qdrant_config = QdrantConfig()


def get_qdrant_client() -> AsyncQdrantClient:
    """Get the global Qdrant client instance."""
    return qdrant_config.get_client()


def get_collection_name() -> str:
    """Get the configured collection name."""
    return qdrant_config.get_collection_name()
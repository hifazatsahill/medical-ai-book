import pytest
from fastapi.testclient import TestClient
from src.api.main import app


def test_health_endpoint():
    """Test the health check endpoint"""
    client = TestClient(app)
    
    response = client.get("/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_root_endpoint():
    """Test the root endpoint"""
    client = TestClient(app)
    
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome" in data["message"]
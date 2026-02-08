from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_status():
    response = client.get("/api/v1/chat/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "ollama_available" in data

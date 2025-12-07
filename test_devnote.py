# tests/testfile.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# def test_trigger_error():
#    response = client.get("/trigger-error")
#    assert response.status_code == 500

def test_stats_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


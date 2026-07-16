import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    
    # Confirm it is deleted
    response2 = client.get("/items/1")
    assert response2.status_code == 404

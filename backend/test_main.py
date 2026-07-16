import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_and_get_item():
    # Create an item first to ensure isolation and a known state
    item_data = {"name": "Test Item", "description": "This is a test item."}
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 200 # Or 201, depending on FastAPI implementation
    created_item = create_response.json()
    item_id = created_item["id"]

    # Now, get the item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == item_data["name"]
    assert response.json()["description"] == item_data["description"]
    assert response.json()["id"] == item_id
    
    # Clean up the created item (optional, but good for test isolation)
    client.delete(f"/items/{item_id}")

def test_create_and_delete_item():
    # Create an item first to ensure isolation and a known state
    item_data = {"name": "Item to Delete", "description": "This item will be deleted."}
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 200
    created_item = create_response.json()
    item_id = created_item["id"]

    # Delete the created item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Item {item_id} deleted"
    
    # Confirm it is deleted
    response2 = client.get(f"/items/{item_id}")
    assert response2.status_code == 404
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

# Initialize items_db with Item objects for consistency and type safety
items_db: List[Item] = [
    Item(id=1, name="Laptop", price=999.99),
    Item(id=2, name="Mouse", price=19.99)
]

@app.get("/items", response_model=List[Item])
def get_items():
    # Fix: items_db now contains Item objects, so it directly matches the response_model.
    # Pydantic will handle the serialization from Item objects to JSON array of objects.
    return items_db

@app.get("/items/{item_id}", response_model=Item) # Added response_model for consistency
def get_item(item_id: int):
    # Fix: Compare integers directly. Access 'id' attribute of Item object.
    for item in items_db:
        if item.id == item_id:
            return item
    # Fix: Raise 404 with a clear message if item not found.
    raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

@app.post("/items", response_model=Item, status_code=201) # Added response_model and status_code 201 Created
def create_item(item: Item):
    # Fix: Check for duplicate ID before adding to prevent logical errors.
    for existing_item in items_db:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail=f"Item with ID {item.id} already exists")
    
    # Fix: `item` is already a Pydantic Item object due to type hint, append it directly.
    items_db.append(item)
    return item # Return the newly created item as per REST best practices

@app.delete("/items/{item_id}", status_code=204) # Use 204 No Content for successful deletion
def delete_item(item_id: int):
    item_index = -1
    # Fix: Find the index of the item to be deleted to avoid issues when modifying during iteration.
    for i, item in enumerate(items_db):
        if item.id == item_id:
            item_index = i
            break # Found the item, exit loop

    if item_index != -1:
        del items_db[item_index]
        # Fix: For a 204 No Content response, typically no body is returned.
        return Response(status_code=204)
    else:
        # Fix: Raise 404 with a clear message if item not found.
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
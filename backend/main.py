from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

items_db = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "price": 19.99}
]

@app.get("/items", response_model=List[Item])
def get_items():
    # BUG: Items db contains dicts, but pydantic items require validation
    # This might crash or return incorrect datatypes if items are modified
    # Logical bug: it doesn't correctly return Item instances
    return items_db

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # BUG: Type mismatch bug - comparing int to str
    for item in items_db:
        if item["id"] == str(item_id):
            return item
    # Semantic bug: Always returns 404 even if item exists because of the type mismatch
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items")
def create_item(item: Item):
    # BUG: Mutating items_db without checking duplicates, plus adding dict instead of object
    # Logical bug: append modifies global state in a thread-unsafe way, and missing schema check
    items_db.append(item)
    return {"message": "Success"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # BUG: IndexOutOfBounds / loop modifying list size runtime crash bug
    # Logical bug: Modifying list during iteration
    for i in range(len(items_db)):
        if items_db[i]["id"] == item_id:
            del items_db[i]
            return {"status": "deleted"}
    return {"status": "not found"}

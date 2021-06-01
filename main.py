from typing import Optional, List

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World! 👋"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: int,
    q: Optional[str] = Query(
        None,
        # validations (strings)
        min_length=3,
        max_length=10,
        regex="^foo$",
    ),
):
    return {"item_id": item_id, "q": q}


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    q: Optional[List[str]] = Query(
        ["spam", "eggs"],  # or None
        # generic validations and metadata
        alias="item-query",
        title="Query string",
        description=(
            "Query string for the items to search in the database"
            "that have a good match"
        ),
        deprecated=True,
    ),
):
    return {"item_id": item_id, **item.dict(), "q": q}

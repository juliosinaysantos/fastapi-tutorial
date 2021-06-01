from typing import Optional, List, Set

from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World! 👋"}


@app.get("/items/{item_id}")
async def read_item(
    # it's allowed args before *.
    *,
    # the following parameters will be kwargs,
    # even if they don't have a default value.
    item_id: int = Path(
        ...,
        # validations (numbers)
        ge=1,
        lt=1000,
        # metadata
        title="The ID of the item to get",
    ),
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


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="The description of the item",
        max_length=300,
    )
    price: float = Field(
        ...,
        gt=0,
        description="The price must be greater than zero",
    )
    tax: Optional[float] = None
    tags: Set[str] = set()
    image: Optional[List[Image]] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.post("/items/")
async def create_item(
    item: Item,  # for embed use -> item: Item = Body(..., embed=True)
    user: User,
    importance: int = Body(...),
    q: Optional[str] = None,
):
    return {"item": item, "user": user, "importance": importance}


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


@app.post("/images/")
async def create_images(images: List[Image] = Body(..., embed=True)):
    return images

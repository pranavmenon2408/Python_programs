from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/items/")
async def root(q: Annotated[list[str] , Query()] = ["food","barhik"]):
    result = {"items": [{"item_id": "foo", "item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result

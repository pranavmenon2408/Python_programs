from fastapi import FastAPI,Path
from typing import Annotated
from pydantic import BaseModel

app=FastAPI()
class Item(BaseModel):
    name:str
    description:str |None=None
    price:float
    tax:float |None=None

@app.put("/items/{item_id}")
async def root(item_id:Annotated[int, Path(title="Id of item",ge=0,le=1000)],q:str |None=None,item:Item |None=None):
    results={"item_id":item_id}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item})
    return results
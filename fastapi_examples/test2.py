from fastapi import FastAPI

app=FastAPI()

@app.get("/item_id/{item_id}/price/{price}")
async def message(item_id: int,price: float,trial: int | None=None):
    item={"item_id":item_id,"price":price,"trial":trial}
    return item 
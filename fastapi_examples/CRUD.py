from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
data=[]
class Book(BaseModel):
    id:int
    title:str
    author:str
    publisher:str |None=None

@app.post('/book')
async def create(book:Book):
    data.append(book.model_dump())
    return data
@app.get('/list')
async def read():
    return data

@app.get('/book/{id}')
async def get_book(id:int):
    return data[id-1]

@app.put("/book/{id}")
async def update(id:int,book:Book):
    data[id-1]=book
    return data

@app.delete("/book/{id}")
async def deletion(id:int):
    data.pop(id-1)
    return data
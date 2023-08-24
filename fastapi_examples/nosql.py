from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI,status
from pydantic import BaseModel
from typing import List
client=AsyncIOMotorClient("mongodb+srv://triyanmukherjee:fIxjD9QwL6Rs67PD@cluster0.4tj4yw2.mongodb.net/")
database=client.Cluster0
book_collection=database.get_collection("User")
def book_helper(dum)->dict:
     "_id":str(dum["_id"])

class Book(BaseModel):
    bookId:int
    title:str
    author:str
    publisher:str
    class Config:
         schema_extra={"example":{"bookId":1,"title":"book title","author":"Author of said book","publisher":"Publisher of said book"}}
app=FastAPI()
@app.post('/add_new',status_code=status.HTTP_201_CREATED)
async def add_book(book:Book):
    
      
      result = book_collection.insert_one(book.model_dump())
      return {"insertion": book.model_dump()}
@app.get("/books")
async def get_books():
    """Get all books in list form."""
    students=[]
    async for s in book_collection.find():
         students.append(book_helper(s))
    return students   
@app.put("/books/{id}")
async def update_book(id:int,book:Book):
     if(len(book.model_dump())<1):
          return False
     b1=book_collection.find_one({"bookId":id})
     if b1:
          updatebook=book_collection.update_one({"bookId":id},{"$set":book.model_dump()})
          if updatebook:
               return True
          return False
               
          

@app.delete("/books/{id}")
async def remove_book(id:int):
     b1=book_collection.find_one({"bookId":id})
     if b1:
          book_collection.delete_one({"bookId":id})
          return True   

     
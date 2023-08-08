from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI,status
from pydantic import BaseModel,Field
from typing import List
client=AsyncIOMotorClient("mongodb+srv://pranav2408dhruv:h3z42kgGE67eL9c0@cluster0.ddclzkr.mongodb.net/?retryWrites=true&w=majority")
database=client.stray_animals
animal_details=database.get_collection("animal_details")
def animal_helper(detail) -> dict:
    return {"title":detail['title'],"details":detail['details'],"image":detail['image'],"map_marker":detail['map_marker']}

app=FastAPI()
class Detail(BaseModel):
    title:str
    details:str
    image:str
    map_marker:str

@app.post('/add_detail',status_code=status.HTTP_201_CREATED,response_model=Detail)
async def append_detail(det:Detail):
    result=animal_details.insert_one(det.model_dump())
    return det

@app.get('/details')
async def get_details():
    details=[]
    for d in animal_details.find():
        details.append(animal_helper(d))
    return details

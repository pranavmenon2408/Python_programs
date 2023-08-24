from typing import List
from fastapi import FastAPI,status
from datetime import datetime
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
import random
from uuid import UUID,uuid4
import requests
import re


def get_address(url):
    regex = r'q=([\d.-]+),([\d.-]+)'
    match = re.search(regex, url)
    if not match:
        return ""
    
    lat, lng = match.group(1), match.group(2)
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}")
    data = response.json()
    return data.get('display_name', '')

def reverse_geocode(lat, lon):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        address = data.get("display_name", "Address not found")
        return address
    else:
        return f"Error: {response.status_code}"

client=AsyncIOMotorClient("mongodb+srv://triyanmukherjee:fIxjD9QwL6Rs67PD@cluster0.4tj4yw2.mongodb.net/")
database=client.Cluster0
dump=database.get_collection('Dump')
def dumper(dum) -> dict:
      return {
        "createdAt": str(dum['createdAt']),
        "updatedAt":str(dum['updatedAt']),
        "location": dum['location'],
        "image":dum['image'],
        "completed":str(dum['completed']),
        "_id":str(dum['_id'])
        
    }
ids=['64d49e76833fa6c6bee85550','64d49e9b833fa6c6bee85552','64d49eb7833fa6c6bee85554']

class Dump(BaseModel):
      location:str
      image:str
      completed:bool
      
      


app=FastAPI()
@app.post('/add_new',status_code=status.HTTP_201_CREATED)
async def add_dump(dum:Dump):
      r=dum.model_dump()
      r.update({'createdAt':datetime.utcnow()})
      r.update({'updatedAt':datetime.utcnow()})
      res=dump.insert_one(r)
      
      return {"insertion": True}

@app.get('/update_description')
async def descrip():
      records =dump.find()
      async for r in records:
           await dump.update_one({"_id":r['_id']},{"$set":{'description':get_address(r['location'])}})
      




    
      

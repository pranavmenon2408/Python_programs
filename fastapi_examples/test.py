from enum import Enum

from fastapi import FastAPI

class ModelName(str,Enum):
    alexnet="alexnet"
    resnet="resnet"
    lenet="lenet"




bruh=FastAPI()

@bruh.get("/models/{model_name}")

async def message(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name":model_name,"message":"Deep Learning FTW"}
    if model_name.value=="lenet":
        return {"model_name":model_name,"message":"some kind of ml thing"}
    return {"model_name":model_name,"message":"another ml kind of thing"}

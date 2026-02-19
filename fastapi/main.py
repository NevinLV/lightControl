from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from tools import manage_light

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ColorData(BaseModel):
    array1: List[str]
    array2: List[str]
    array3: List[str]


@app.post("/set/")
async def set_color(data: ColorData):

    manage_light.sendCommand(data.array1, data.array2, data.array3)
    return {
        "status": "success",
    }
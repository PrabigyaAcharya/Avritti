from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from genetic_backbone import *
from melody import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST','GET'],
    allow_headers=['*'],
)

# class Data(BaseModel):
#     greeting:str

db=[]

popn = Population(5, 256, fit)  

@app.get("/generate")
def test(details:dict):
    return genome_midi_decoder(popn,)
    

# @app.post("/hello")
# def add_greeting(message:Data):
#     db.append({"Hello":message.greeting})
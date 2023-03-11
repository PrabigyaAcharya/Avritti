from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from genetic_backbone import *
from melody import *

import base64

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

popn = Population(5, 256)  

@app.post("/generate")
def test(details:dict):
    base64_data=[]
    genome_midi_decoder(population=popn,note=details["note"],octave=int(details["octave"]),scale=details["scale"])
    for i in range(len(popn.population)):
        file_name = f"output/testmidi_{str(i)}"
        with open(file_name, "rb") as output_file:
            base64_file = base64.b64encode(output_file.read())
            base64_data.append(base64_file)
    return base64_data

@app.post("/rate")
def test(details:dict):
    return popn.fitness(ratings=details["ratings"])
    

# @app.post("/hello")
# def add_greeting(message:Data):
#     db.append({"Hello":message.greeting})
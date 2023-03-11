from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from genetic_backbone import *

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
popn.fitness() 

@app.get("/generate")
def test(scale):
    for i in range(50):
        if popn.move_generation(debug=False):
            db.append((i, popn.population[0]))
    return db

# @app.post("/hello")
# def add_greeting(message:Data):
#     db.append({"Hello":message.greeting})
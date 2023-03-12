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

db={"note":"D#","octave":"3","scale":"blues"}

popn = Population(5, 256)  

@app.post("/newgen")
def new_gen(details:dict):
    global popn
    popn=Population(5,256)
    return gen(details)

@app.post("/generate")
def gen(details:dict):
    base64_data=[]
    population_midi_generator(population=popn,root_note=details["note"],octave=int(details["octave"]),scale=details["scale"])
    db["note"]=details["note"]
    db["octave"]=details["octave"]
    db["scale"]=details["scale"]
    for i in range(len(popn.population)):
        file_name = f"output/testmidi_{str(i)}"
        with open(file_name, "rb") as output_file:
            base64_file = base64.b64encode(output_file.read())
            base64_data.append(base64_file)
    return {"generation":popn.generation_number,"midiList":base64_data}

@app.post("/rate")
def rate(details:dict):
    if(details["stop"]==False):
        popn.fitness(ratings=details["ratings"])
        popn.move_generation(debug=False)
        return gen(db)
    else:
        index=details["ratings"].index(max(details["ratings"]))
        file_name = f"output/testmidi_{str(index)}"
        with open(file_name, "rb") as output_file:
            return base64.b64encode(output_file.read())


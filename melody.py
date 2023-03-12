import random
from midiutil import MIDIFile
from genetic_backbone import Genome,Population
import pyo


NOTES_LIST =["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PAUSE_PROBABILITY = 0.2

def genome_to_notes(genome, bits_per_note, num_of_notes):
    notes = [genome.genome[i:i+bits_per_note] for i in range(num_of_notes)]
    int_notes = [sum([bit*pow(2, index) for index, bit in enumerate(note)]) for note in notes]
    return int_notes


def population_midi_generator(population, root_note:str = "C", octave:int = 3, bits_per_note=4, num_of_notes=64, scale:str = "lydian", chord_step = 3):
    count = 0
    is_pausing = PAUSE_PROBABILITY > random.random()

    note_length = 4/ float(num_of_notes)

    #good_notes = musical_scales.scale(starting_note=note, octaves=octave, mode = scale)
    scl = pyo.EventScale(root=root_note, 
                         scale = scale, 
                         first=octave * (NOTES_LIST.index(root_note)+1),
                         octaves=2)
    print(
        f"Root note {root_note} and first = {octave * NOTES_LIST.index(root_note)+1}")
    for genome in population.population:

        melody = {
            "notes": [],
            "velocity": [],
            "beat": []
        }
        notes = genome_to_notes(genome, bits_per_note, num_of_notes)
        for note in notes:
            if not is_pausing:
                note = int(note %pow(2, bits_per_note-1))

            if  note>= pow(2, bits_per_note - 1):
                melody["notes"] += [0]
                melody["velocity"] += [0]
                melody["beat"] += [note_length]
            else:
                if len(melody["notes"]) > 0 and melody["notes"][-1] == note:
                    melody["beat"][-1] +=note_length
                else:
                    melody["notes"] += [note]
                    melody["velocity"] += [127]
                    melody["beat"] += [note_length]
        steps = []
        for step in range(chord_step):
            steps.append([scl[(note+step*2) % len(scl)]
                        for note in melody["notes"]])
        melody["notes"] = steps
        
        mf = MIDIFile(1)
        track = 0
        channel = 0
        time = 0.0
        tempo = 120

        mf.addTrackName(track, time, "sampletrack")
        mf.addTempo(track, time, 60)

        for i, vel in enumerate(melody["velocity"]):
            if vel > 0:
                for step in melody["notes"]:
                    mf.addNote(track, channel, step[i],
                               time+i, melody["beat"][i], vel)

            time += melody["beat"][i]
        with open(f"output/test_{count}.mid", "wb") as f:
            mf.writeFile(f)
        print(count)
        count +=1

popn = Population(4, 256)
print(population_midi_generator(popn))


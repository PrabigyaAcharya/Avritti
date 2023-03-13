import random
from midiutil import MIDIFile
from genetic_backbone import Genome,Population
import pyo


NOTES_LIST =["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PAUSE_PROBABILITY = 0.2

def genome_to_notes(genome, bits_per_note, num_of_notes):
    notes = [genome.genome[i*bits_per_note:i*bits_per_note+bits_per_note] for i in range(num_of_notes)]
    int_notes = [sum([bit*pow(2, index) for index, bit in enumerate(note)]) for note in notes]
    velocity_values = [genome.genome[i*bits_per_note:i*bits_per_note +
                                     bits_per_note] for i in range(num_of_notes, num_of_notes*2)]
    int_velo = [5 * sum([bit*pow(2, index) for index,
                        bit in enumerate(note)]) + 25 for note in velocity_values]
    return int_notes, int_velo


def population_midi_generator(population, root_note:str = "C", octave:int = 4, bits_per_note=4, num_of_notes=32, scale:str = "major", chord_step = 2):
    count = 0
    is_pausing = PAUSE_PROBABILITY > random.random()

    note_length = 4/float(bits_per_note)

    scl = pyo.EventScale(root=root_note, 
                         scale = scale, 
                         first=octave * (NOTES_LIST.index(root_note)+1),
                         octaves=2)
    print(f"Root note {root_note} and first = {octave * NOTES_LIST.index(root_note)+1}")
    for genome in population.population:

        melody = {
            "notes": [],
            "velocity": [],
            "beat": []
        }
        notes, velocities = genome_to_notes(genome, bits_per_note, num_of_notes)
        for j, note in enumerate(notes):
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
                    melody["velocity"] += [velocities[j]]
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

        mf.addTrackName(track, time, "sampletrack")
        mf.addTempo(track, time, 120)

        for i, vel in enumerate(melody["velocity"]):
            if vel > 0:
                for step in melody["notes"]:
                    mf.addNote(track, channel, step[i],
                               time, melody["beat"][i], vel)

            time += melody["beat"][i]

        with open(f"output/testmidi_{count}", "wb") as f:
            mf.writeFile(f)

        count +=1

import random
from midiutil import MIDIFile
from genetic_backbone import Genome, Population
import musical_scales

def fit():
    return random.randint(1, 5)


def genome_midi_decoder(population, note:str = "C", octave:int = 3, bits_per_note=4, num_of_notes=64, scale:str = "major"):

    good_notes = musical_scales.scale(starting_note=note, octaves=octave, mode = scale)
    track = 0
    channel = 0
    time = 0    # In beats
    duration = 1    # In beats
    tempo = 60   # In BPM
    volume = 100  # 0-127, as per the MIDI standard
    count = 0
    try:
        for genome in population.population:
            notes = [genome.genome[i:i+bits_per_note] for i in range(num_of_notes)]
            midinotes = [60+sum([bit*pow(2, index)
                                for index, bit in enumerate(note)]) for note in notes]
            MyMIDI = MIDIFile(1)  
            MyMIDI.addTempo(track, time, tempo)

            for i, pitch in enumerate(midinotes):
                MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
            
            file_name = "testmidi_" + str(count)
            count+=1
            with open(file_name, "wb") as output_file:
                MyMIDI.writeFile(output_file)
    except:
        return False
    return True


import mido as md

midi = md.MidiFile("Data/MIDI FILES/Raw/A Major/01AMAJ.mid") # Initialzes a midi file
print("New Midi file created")

def midi_data(midi_track):
    for i, track in enumerate(midi_track): # Gives a structure for our midi file
        print(f"Track {i}: {track.name}")
        for msg in track:
            if ((list(str(msg))[0])=="n"):
                print(msg)
            else:
                pass

midi_data(midi.tracks)
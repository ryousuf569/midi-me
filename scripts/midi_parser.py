import mido as md

midi = md.MidiFile("Data/MIDI FILES/Raw/A Major/01AMAJ.mid") # Initialzes a midi file
print("New Midi file created")


def midi_data(midi_track):
    midi_data_list = list()
    for i, track in enumerate(midi_track):
        for msg in track:
            if ((list(str(msg))[0])=="n"):
                midi_data_list.append(str(msg))
            else:
                pass
    return midi_data_list

nigger = md.Message.from_str(midi_data(midi.tracks)[0])
print(nigger)
print(nigger.note)
import mido as md

midi = md.MidiFile("Data/MIDI FILES/Raw/A Major/01AMAJ.mid") # Initialzes a midi file
print("New Midi file created")


def midi_data(midi_track):
    midi_data_list = list()
    midi_data_note = list()
    midi_data_time = list()
    midi_data_vel = list()
    for i, track in enumerate(midi_track):
        print(f"Track {i}: {track.name}")
        for msg in track:
            if ((list(str(msg))[0])=="n"):
                midi_data_list.append(msg.type)
                midi_data_note.append(msg.note)
                midi_data_time.append(msg.time)
                midi_data_vel.append(msg.velocity)
            else:
                pass
    return midi_data_list, midi_data_note, midi_data_time, midi_data_vel

(print(midi.ticks_per_beat))
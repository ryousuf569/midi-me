from pathlib import Path
import pretty_midi
import json
import os

major_keys = [
    "C major", "Db major", "D major", "Eb major", "E major", "F major",
    "Gb major", "G major", "Ab major", "A major", "Bb major", "B major"
]

minor_keys = [
    "C minor", "C# minor", "D minor", "Eb minor", "E minor", "F minor",
    "F# minor", "G minor", "G# minor", "A minor", "Bb minor", "B minor"
]

all_keys = major_keys + minor_keys

print(all_keys)

selected_key = input("Which key do you want? ")
selected_for_key_num = selected_key.strip().lower()
all_keys_lower = [k.lower() for k in all_keys]
key_number = all_keys_lower.index(selected_for_key_num)

print(key_number)

midi_repo_root = Path(__file__).parent.parent
raw_midi_folder = midi_repo_root / "Data" / "MIDI FILES"/ "Raw" / selected_key
midi_files = raw_midi_folder.rglob('*.mid')
midi_list = list(midi_files)

midi_file = pretty_midi.PrettyMIDI(str(midi_list[0]))
midi_program = pretty_midi.instrument_name_to_program('Piano')
midi_key = pretty_midi.KeySignature(key_number, 0.0)
midi_timesig = pretty_midi.TimeSignature(4 ,4, 0.0)



from pathlib import Path

selected_key = input("Which key do you want? ")

midi_repo_root = Path(__file__).parent.parent
raw_midi_folder = midi_repo_root / "Data" / "MIDI FILES"/ "Raw" / selected_key
midi_files = raw_midi_folder.rglob('*.mid')

for midi in midi_files:
    print(repr(midi.name))
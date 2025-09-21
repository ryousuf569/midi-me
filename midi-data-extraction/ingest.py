from pathlib import Path

midi_repo_root = Path(__file__).parent.parent
raw_midi_folder = midi_repo_root / "Data" / "MIDI FILES"/ "Raw"
midi_files = raw_midi_folder.rglob('*.mid')

for midi in midi_files:
    print(repr(midi.name))
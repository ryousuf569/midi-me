import mido as md
from collections import defaultdict
import pandas as pd
import numpy as np

midi = md.MidiFile("MarvinsRoom.mid") # Initialzes a midi file
print("New Midi file created")


def midi_data(midi_tracks):
    midi_data_list = []
    midi_data_note = []
    midi_data_time = []
    midi_data_vel = []
    abs_time = 0 

    for i, track in enumerate(midi_tracks):
        for msg in track:
            abs_time += msg.time
            if msg.type == "note_on":
                midi_data_list.append(msg)
                midi_data_note.append(msg.note)
                midi_data_time.append(abs_time)
                midi_data_vel.append(msg.velocity)
            if msg.type == "note_off":
                midi_data_list.append(msg)
            

    return midi_data_list, midi_data_note, midi_data_time, midi_data_vel


def get_midi_df(note_list, time_list, velocity_list):

    notes = []
    chords = defaultdict(list)

    for note, time, vel in zip(note_list, time_list, velocity_list):
        notes.append({
            "note": note,
            "start": time,
            "velocity": vel})

    for n in notes:
        n["beat"] = n["start"] / tpb
        n["bar"] = int(n["beat"] // 4)
        n["pitch_class"] = n["note"] % 12
        chords[n["start"]].append(n["note"])

    return pd.DataFrame(notes)

def state_features(df):

    bars = df.groupby("bar")
    states = []

    for bar, g in bars:
        pitches = g["note"].tolist()
        pcs = g["pitch_class"].tolist()

        states.append({
        "bar": bar,
        "note_density": len(g),
        "pitch_range": max(pitches) - min(pitches),
        "pitch_entropy": -sum(
            (pcs.count(pc)/len(pcs)) * np.log2(pcs.count(pc)/len(pcs))
            for pc in set(pcs)), 
            # using Shannon entropy to measure how spread out the notes are across pitch classes
        "chord_size": len(set(pitches)),
        "mean_pitch": np.mean(pitches),})
    
    return pd.DataFrame(states)

def delta_features(df):
    # measures change between consecutive bars
    deltas = []

    for i in range(len(df) - 1):

        a = df.iloc[i]
        b = df.iloc[i + 1]

        deltas.append({
            "bar": a["bar"],
            "delta_density": abs(a["note_density"] - b["note_density"]),
            "delta_pitch_range": abs(a["pitch_range"] - b["pitch_range"]),
            "delta_entropy": abs(a["pitch_entropy"] - b["pitch_entropy"]),})
        
    return pd.DataFrame(deltas)

def build_graph(sdf, deltadf):

    graph = {}

    for i in range(len(sdf) - 1):

        graph[i] = {
            "next": i + 1,
            "fatigue_cost": (
                deltadf.iloc[i]["delta_entropy"] * 0.4 +
                deltadf.iloc[i]["delta_density"] * 0.3 +
                deltadf.iloc[i]["delta_pitch_range"] * 0.3)}

    return graph


message_list, note_list, time_list, velocity_list = midi_data(midi.tracks)
tpb = midi.ticks_per_beat
df = get_midi_df(note_list, time_list, velocity_list)
state_df = state_features(df)
delta_df = delta_features(state_df)

graph = build_graph(state_df, delta_df)
print(graph)
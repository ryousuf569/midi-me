import librosa
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sqlite3

def make_stem_graph(path):

    def load_stem(path, sr=22050, mono=True):
        # y is us loading the waveform and sr is sample rate
        y, sr = librosa.load(path, sr=sr, mono=mono)
        y = librosa.util.normalize(y)
        return y, sr
    
    def stem_features(y, sr, hop_length=512):

        # STFT magnitude, represents a signal in the time-frequency domain
        S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop_length))

        rms = librosa.feature.rms(S=S)[0] # perceived loudness
        centroid = librosa.feature.spectral_centroid(S=S, sr=sr)[0] # brightness
        bandwidth = librosa.feature.spectral_bandwidth(S=S, sr=sr)[0] # spread
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)[0] # noisy/edgy

        # how “eventful”
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
        # how fast the spectrum changes
        flux = librosa.onset.onset_strength(
            S=librosa.power_to_db(S**2),
            sr=sr,
            hop_length=hop_length)

        times = librosa.frames_to_time(
            np.arange(len(rms)), sr=sr, hop_length=hop_length)

        return {
        "times": times,
        "energy": rms,
        "brightness": centroid,
        "bandwidth": bandwidth,
        "noise": zcr,
        "onset": onset_env,
        "spectrum_changes": flux, }
    
    def featurenodes(features, window=1.0):
        times = features["times"]
        max_t = times[-1]

        nodes = []
        t = 0.0

        while t < max_t:

            mask = (times >= t) & (times < t + window)
            if not np.any(mask):
                t += window
                continue

            node = {
            "time": t,
            "energy": np.mean(features["energy"][mask]),
            "energy_var": np.var(features["energy"][mask]),
            "brightness": np.mean(features["brightness"][mask]),
            "bandwidth": np.mean(features["bandwidth"][mask]),
            "noise": np.mean(features["noise"][mask]),
            "onset_rate": np.sum(features["onset"][mask]),
            "spectrum_changes": np.mean(features["spectrum_changes"][mask]),}

            nodes.append(node)
            t += window

        return nodes

    def audio_graph(nodes): 
        graph = {}

        for i in range(len(nodes) - 1):
            a = nodes[i]
            b = nodes[i + 1]

            fatigue = (
                abs(a["energy"] - b["energy"]) * 0.3 +
                abs(a["brightness"] - b["brightness"]) * 0.3 +
                abs(a["spectrum_changes"] - b["spectrum_changes"]) * 0.4)

            graph[i] = {
                "next": i + 1,
                "fatigue_cost": fatigue,
                "energy" : abs(a["energy"] - b["energy"]) * 0.3,
                "brightness": abs(a["brightness"] - b["brightness"]) * 0.3,
                "spectrum_changes" : abs(a["spectrum_changes"] - b["spectrum_changes"]) * 0.4}  
            
        return graph
    
    y, sr = load_stem(path)
    features = stem_features(y, sr)
    nodes = featurenodes(features)

    return audio_graph(nodes)

drum_graph = make_stem_graph("tempstems/SpotiDownloader.com - Assumptions - Sam Gellaitry_drums.wav")
bass_graph = make_stem_graph("tempstems/SpotiDownloader.com - Assumptions - Sam Gellaitry_bass.wav")
other_graph = make_stem_graph("tempstems/SpotiDownloader.com - Assumptions - Sam Gellaitry_other.wav")
vocal_graph = make_stem_graph("tempstems/SpotiDownloader.com - Assumptions - Sam Gellaitry_vocals.wav")

def extract_component_arrays(graph):
    keys = sorted(graph.keys())

    return {
        "energy": np.array([graph[k]["energy"] for k in keys]),
        "brightness": np.array([graph[k]["brightness"] for k in keys]),
        "spectrum_changes": np.array([graph[k]["spectrum_changes"] for k in keys])
    }


def mean_song_graph(*graphs):

    component_arrays = [extract_component_arrays(g) for g in graphs]

    # find shortest stem so everything aligns in time
    min_len = min(len(c["energy"]) for c in component_arrays)

    # trim all arrays
    for c in component_arrays:
        for key in c:
            c[key] = c[key][:min_len]

    # stack + mean each component
    mean_energy = np.mean(
        np.stack([c["energy"] for c in component_arrays], axis=0),
        axis=0
    )

    mean_brightness = np.mean(
        np.stack([c["brightness"] for c in component_arrays], axis=0),
        axis=0
    )

    mean_spectrum = np.mean(
        np.stack([c["spectrum_changes"] for c in component_arrays], axis=0),
        axis=0
    )

    # reconstruct song graph
    song_graph = {}
    for i in range(min_len):
        fatigue_cost = (
            mean_energy[i]
            + mean_brightness[i]
            + mean_spectrum[i]
        )

        song_graph[i] = {
            "next": i + 1 if i < min_len - 1 else None,
            "fatigue_cost": float(fatigue_cost),
            "energy": float(mean_energy[i]),
            "brightness": float(mean_brightness[i]),
            "spectrum_changes": float(mean_spectrum[i])
        }

    return song_graph

song_graph = mean_song_graph(
    drum_graph,
    bass_graph,
    other_graph,
    vocal_graph)

mm = MinMaxScaler()

song_id = 4
df = pd.DataFrame(song_graph).T
df["song_id"] = song_id

fatigue_to_scale = df["fatigue_cost"].values.reshape(-1, 1)
scaled_fatigue = mm.fit_transform(fatigue_to_scale)
df["fatigue_cost"] = scaled_fatigue

energy_to_scale = df["energy"].values.reshape(-1, 1)
scaled_energy = mm.fit_transform(energy_to_scale)
df["energy"] = scaled_energy

brightness_to_scale = df["brightness"].values.reshape(-1, 1)
scaled_brightness = mm.fit_transform(brightness_to_scale)
df["brightness"] = scaled_brightness

sc_to_scale = df["spectrum_changes"].values.reshape(-1, 1)
scaled_sc = mm.fit_transform(sc_to_scale)
df["spectrum_changes"] = scaled_sc

db_path = 'data/midi_me.db'
conn = sqlite3.connect(db_path)
df.to_sql("audio_fatigue",
                     conn,
                     if_exists="append",
                     index=False)
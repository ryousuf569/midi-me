import librosa
import numpy as np

def make_stem_graph(path):

    def load_stem(path, sr=22050, mono=True):
        y, sr = librosa.load(path, sr=sr, mono=mono) # y is us loading the waveform and sr is sample rate
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
                "fatigue_cost": fatigue}  
            
        return graph
    
    y, sr = load_stem(path)
    features = stem_features(y, sr)
    nodes = featurenodes(features)
    return audio_graph(nodes)

print(make_stem_graph("tempstems/Marvins Room_drums.wav"))
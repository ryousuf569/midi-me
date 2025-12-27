import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/midi_me.db")
cursor = conn.cursor()
sql_query = "SELECT song_id, next, fatigue_cost, energy, brightness, spectrum_changes FROM audio_fatigue WHERE song_id=2"


df = pd.read_sql(sql_query, conn)

W = 15 # Window for rolling averages

# we taking rolling averages and variance of each metric to then later compute scores that help
# determining engagement states

df["energy_mean"] = (
    df.groupby("song_id")["energy"]
      .rolling(W, min_periods=1)
      .mean()
      .reset_index(level=0, drop=True))

df["brightness_mean"] = (
    df.groupby("song_id")["brightness"]
      .rolling(W, min_periods=1)
      .mean()
      .reset_index(level=0, drop=True))

df["spectrum_mean"] = (
    df.groupby("song_id")["spectrum_changes"]
      .rolling(W, min_periods=1)
      .mean()
      .reset_index(level=0, drop=True))

df["fatigue_mean"] = (
    df.groupby("song_id")["fatigue_cost"]
      .rolling(W, min_periods=1)
      .mean()
      .reset_index(level=0, drop=True))

df["fatigue_var"] = (
    df.groupby("song_id")["fatigue_cost"]
      .rolling(W, min_periods=2)
      .var()
      .reset_index(level=0, drop=True)
      .fillna(0))

df["spectrum_var"] = (
    df.groupby("song_id")["spectrum_changes"]
      .rolling(W, min_periods=2)
      .var()
      .reset_index(level=0, drop=True)
      .fillna(0))

# we use 2 decimal coefficients that add up to 1 so that the values stay between 0 and 1 as desired

# energy tends to matter more than brightness for “loud/active” feel
df["intensity"] = 0.6 * df["energy_mean"] + 0.4 * df["brightness_mean"]

# using the change related signals to get a sense of how much the song is changing per second
df["novelty"] = 0.5 * df["spectrum_mean"] + 0.5 * df["fatigue_mean"]

# higher value -> more stationary
# originally all these values were higher than desired, so we divide it with the 90th percentile to normalize it
df["stationarity"] = 1 - (((0.5 * df["fatigue_var"]) + (0.5 * df["spectrum_var"])) / np.percentile(((0.5 * df["fatigue_var"]) + (0.5 * df["spectrum_var"])), 90)).clip(0, 1)

def classify_state(row):
    if row["intensity"] < 0.2 and row["stationarity"] > 0.68:
        return "boring"
    elif row["novelty"] < 0.2 and row["stationarity"] > 0.68:
        return "boring"
    elif row["intensity"] > 0.4 and row["stationarity"] > 0.68:
        return "overstimulating"
    elif row["novelty"] > 0.4 and row["stationarity"] > 0.68:
        return "overstimulating"
    else:
        return "engaging"

df["state"] = df.apply(classify_state, axis=1)

df.to_csv('data/song_analysis.csv')
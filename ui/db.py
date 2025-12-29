import sqlite3
import pandas as pd

db_path = 'data/midi_me.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

metadata_df = pd.read_sql("SELECT * FROM songs WHERE song_id=1", conn)
artist = metadata_df["artist"].iloc[0]
title = metadata_df["title"].iloc[0]

cursor.execute("SELECT risk_curve FROM risk_curve WHERE id=1")
risk_curve = [row[0] for row in cursor.fetchall()]

fatigue_df = pd.read_sql("SELECT fatigue_cost, brightness, energy, spectrum_changes FROM audio_fatigue WHERE song_id = 1", conn)
fatigue = fatigue_df["fatigue_cost"].to_numpy()
energy = fatigue_df["energy"].to_numpy()
brightness = fatigue_df["brightness"].to_numpy()
spectrum_changes = fatigue_df["spectrum_changes"].to_numpy()

df = pd.read_sql("SELECT * FROM simulated_stats", conn)




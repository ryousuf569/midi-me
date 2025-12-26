import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("data/midi_me.db")
cursor = conn.cursor()

cursor.execute("SELECT brightness FROM audio_fatigue WHERE run_id=1")
y1_values = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT energy FROM audio_fatigue WHERE run_id=1")
y2_values = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT fatigue_cost FROM audio_fatigue WHERE run_id=1")
y3_values = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT spectrum_changes FROM audio_fatigue WHERE run_id=1")
y4_values = [row[0] for row in cursor.fetchall()]

plt.figure(figsize=(8, 4))
plt.plot(y1_values, label="energy")
plt.plot(y2_values, label="brightness")
plt.plot(y3_values, label="fatigue_cost")
plt.plot(y4_values, label="spectrum_changes")
plt.xlabel("seconds")
plt.title("Audio Stats per Second")
plt.grid(True)
plt.tight_layout()
plt.show()
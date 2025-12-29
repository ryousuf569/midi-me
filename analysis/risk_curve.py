import sqlite3
import pandas as pd
import numpy as np

def risk_curve():
    conn = sqlite3.connect("data/midi_me.db")
    cursor = conn.cursor()

    df = pd.read_csv('data/state_analysis.csv')

    run = pd.read_sql("SELECT * FROM simulated_stats", conn)
    run["start"] = run["start"].astype(int)
    run["end"]   = run["end"].astype(int)

    transitions = df["state"].tolist()
    cursor.execute("SELECT fatigue_cost FROM audio_fatigue WHERE song_id=1")

    def mean_fatigue(row):
        s = int(row.start)
        e = int(row.end) + 1
        return fatigue_list[s:e].mean()

    def transition_risk(state):
        if state == 1: 
            return T[1,1]
        else: 
            return T[0,1]
    
    T = (pd.crosstab(
        pd.Series(transitions[:-1], name='From'), # current state
        pd.Series(transitions[1:], name='To'), # next state
        normalize=0)).to_numpy() # normalize across each row
    T = np.clip(T, 1e-12, 1.0)
    T = T ** 0.6   

    T = T / T.sum(axis=1, keepdims=True)
    fatigue_list = pd.DataFrame([row[0] for row in cursor.fetchall()])
    x, y, z = 0.4, 0.4, 0.2

    run["duration"] = run["end"] - run["start"] + 1
    run["mean_fatigue"] = run.apply(mean_fatigue, axis=1)
    run["transition_risk"] = run["state"].apply(transition_risk)
    run["curve_score"] = (
        x * run["mean_fatigue"] +
        y * run["transition_risk"] +
        z * (run["duration"] / run["duration"].max()))

    risk_curve = np.zeros(len(fatigue_list))
    for _, row in run.iterrows():
        s = int(row.start)
        e = int(row.end) + 1
        risk_curve[s:e] = row.curve_score
    
    risk_curve_df = pd.DataFrame(risk_curve, columns=["risk_curve"])
    risk_curve_df["id"] = run["id"].iloc[0]
    risk_curve_df.to_sql("risk_curve",
                        conn,
                        if_exists="replace",
                        index=False)
    
risk_curve()
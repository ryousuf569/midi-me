import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.utils.class_weight import compute_class_weight

def simulated_stats(id):
    df = pd.read_csv('data/state_analysis.csv')
    run4 = df[df["song_id"]== id].copy()
    states = [0, 1, 2]
    transitions = df["state"].tolist()

    FEATURES = ["energy", "brightness", "spectrum_changes", "fatigue_cost"]
    STATE_ORDER = ["boring", "engaging", "overstimulating"]

    X = df[FEATURES].values
    y = df["state"].values 

    # since O barely shows up in the data, we had to add some weight
    # to it for emission probability, otherwise even when a song is
    # overstimulating, viterbi alg will never visit 2 
    classes = np.array(["boring", "engaging", "overstimulating"])
    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y)

    class_weight = {i: w for i, w in zip(classes, weights)}

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            multi_class="multinomial",
            solver="lbfgs",
            max_iter=200,
            class_weight=class_weight))
    ])

    pipe.fit(X, y)

    def build_emissions(song_df, model):

        X = song_df[FEATURES].values
        emissions = model.predict_proba(X)

        # safety floor
        eps = 1e-6
        emissions = np.clip(emissions, eps, 1.0)
        emissions /= emissions.sum(axis=1, keepdims=True)

        return emissions

    def soften_transitions(P, alpha=0.6, eps=1e-12):
        '''
        i noticed boring, and engaging states HEAVILY favor self loops,
        so I did some research and found I should soften the matrix using numpy
        '''
        P = np.clip(P, eps, 1.0)
        P = P ** alpha           
        return P / P.sum(axis=1, keepdims=True)

    emissions_matrix = (build_emissions(run4, pipe))
    transition_matrix = (pd.crosstab(
        pd.Series(transitions[:-1], name='From'), # current state
        pd.Series(transitions[1:], name='To'), # next state
        normalize=0)).to_numpy() # normalize across each row

    def viterbi(emissions, P, pi):

        T, S = emissions.shape
        # T = number of time steps (seconds)
        # S = number of hidden states (e.g., boring / engaging / overstimulating)
        dp = np.zeros((T, S))
        backptr = np.zeros((T, S), dtype=int)
        # backptr[t, s] = argmax previous state that led to state s at time t

        dp[0] = np.log(pi) + np.log(emissions[0])

        for t in range(1, T):
            for s in range(S):
                scores = dp[t-1] + np.log(P[:, s])
                backptr[t, s] = np.argmax(scores)
                dp[t, s] = scores[backptr[t, s]] + np.log(emissions[t, s])

        states = np.zeros(T, dtype=int)
        states[-1] = np.argmax(dp[-1])

        for t in range(T-2, -1, -1):
            states[t] = backptr[t+1, states[t+1]]

        return states

    def extract_zones(state_seq, min_len=7):
        zones = []
        start = 0

        for t in range(1, len(state_seq)):
            if state_seq[t] != state_seq[t-1]:
                if t - start >= min_len:
                    zones.append((int(state_seq[start]), start, t-1))
                start = t

        if len(state_seq) - start >= min_len:
            zones.append((int(state_seq[start]), start, len(state_seq)-1))

        return zones

    def zone_risk(state, length, P, state_map):
        i = state_map[state]

        exit_risk = 1 - P[i, i]
        expected_duration = 1 / (1 - P[i, i])
        risk = (
            exit_risk * 0.4 +
            (length / expected_duration) * 0.4 +
            (state != 1) * 0.2
        )

        return float(risk)

    st_matrix = soften_transitions(transition_matrix, alpha=0.6)
    states_per_s = viterbi(emissions_matrix, st_matrix, np.array([0.6, 0.3, 0.1]))
    zones = extract_zones(states_per_s)

    zones_risk_score = [
        (state, start, end, round((zone_risk(state, end-start+1, st_matrix, states)), 3))
        for state, start, end in zones]

    conn = sqlite3.connect("data/midi_me.db")
    songdf = pd.DataFrame(zones_risk_score, columns=["state", "start", "end", "risk_score"])
    songdf["id"] = id
    songdf.to_sql("simulated_stats",
                        conn,
                        if_exists="replace",
                        index=False)
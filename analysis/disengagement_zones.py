import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv('data/state_analysis.csv')
run4 = df[df["song_id"]== 4].copy()

transitions = df["state"].tolist()

''' using a multinomial logistic regression model to get emission probabilities
    after reading GeeksforGeeks, I saw an MLR outputs a normalized probablity vector, 
    which is CRITICAL for probablistic simulation with my agents later on, it is a light
    Ml model that works well for classification, which is what I'm working with right now.'''

FEATURES = ["energy", "brightness", "spectrum_changes", "fatigue_cost"]
STATE_ORDER = ["boring", "engaging", "overstimulating"]

X = df[FEATURES].values
y = df["state"].values 

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(
        multi_class="multinomial",
        solver="lbfgs",
        max_iter=200
    ))
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

emissions_matrix = build_emissions(run4, pipe)
transition_matrix_df = (pd.crosstab(
    pd.Series(transitions[:-1], name='From'), # current state
    pd.Series(transitions[1:], name='To'), # next state
    normalize=0)).to_numpy() # normalize across each row

print(emissions_matrix)
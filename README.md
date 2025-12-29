# MIDI.me — Listener Engagement & Disengagement Analysis

**Demo:** `./demo.gif`

MIDI.me is an interpretable music-analysis system that detects **listener disengagement regions** in songs by modeling audio features with a **Hidden Markov Model (HMM)** and producing a **per-second disengagement risk score**.  
The system is designed to support **time-localized, explainable creative decisions**, not black-box predictions.

---

## 🔍 What This Project Does

- Identifies **high-risk disengagement regions** covering **~18–25% of track duration** across **40 songs**
- Infers latent listener engagement states over time using **HMM + Viterbi**
- Produces an **interpretable per-second disengagement risk signal**
- Aligns high-risk segments with **manually annotated disengagement regions in 7 / 10 evaluated tracks**
- Supports interactive, song-level analysis through a local visualization pipeline

---

## 🧠 Core Modeling Approach

### 1. Audio Feature Extraction
Audio features are extracted using `librosa` at a fine temporal resolution (per-second), including:
- Energy
- Brightness
- Spectral change
- Fatigue indicators

These features capture both instantaneous intensity and longer-term listener fatigue.

---

### 2. Engagement State Modeling (HMM + Viterbi)

- Listener engagement is modeled as **latent discrete states** in a **Hidden Markov Model**
- The **Viterbi algorithm** is used to infer the most likely engagement state sequence over time
- This enables **time-localized interpretation** (e.g., identifying *where* and *why* disengagement occurs)

---

### 3. Emission Probability Estimation

- **Multinomial Logistic Regression** is used to estimate HMM emission probabilities
- Provides a **transparent mapping** from continuous audio features → engagement states
- Prioritizes interpretability over opaque deep learning models

---

### 4. Disengagement Risk Scoring

A per-second disengagement risk score is computed by weighting:
- Inferred engagement states
- Markov transition likelihoods
- Fatigue-related features

This produces a continuous risk signal suitable for visualization and downstream analysis.

---

## 📊 Visualization & Analysis Pipeline

- Local visualization tools for:
  - Engagement state timelines
  - Disengagement risk curves
  - Song-level and run-level comparisons
- Backed by a **relational database**
  - `song_id` used as a primary key
  - Tracks engagement runs across experiments
  - Enables reproducible, interactive analysis

---

## 📘 Model Intuition & Theory

This project emphasizes **interpretability and causal reasoning** so results can directly inform creative decisions.

Detailed explanations are provided for:
- Engagement state design
- HMM structure and transition dynamics
- Emission modeling with multinomial logistic regression
- Disengagement risk formulation
- Design tradeoffs and modeling assumptions

👉 See the `research/` folder for full mathematical and conceptual details.

---

## 🛠 Tech Stack

- Python
- librosa
- NumPy / pandas
- scikit-learn
- Relational database (SQLite / PostgreSQL)
- Matplotlib and custom visualization tools

---

## 🎯 Use Cases

- Music producers identifying listener drop-off points
- Comparing multiple versions of a track
- Data-driven creative iteration
- Portfolio-grade example of interpretable sequential modeling

---

## 🚀 Status & Future Work

Planned extensions include:
- Larger datasets and cross-genre evaluation
- Real-time analysis
- Plugin / DAW-integrated workflows
- Deeper modeling of long-range listener fatigue

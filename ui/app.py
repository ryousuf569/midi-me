# py -m streamlit run C:\Users\ryous\Downloads\MIDI-ME\ui\app.py
import streamlit as st
from plots import *
from db import *

fig1 = basic_plot(fatigue, energy, brightness, spectrum_changes)
fig2 = risk_curve_plot(risk_curve)
fig3 = engagement_heatmap(df, 1)

st.title("Listener Engagement Analysis")
st.subheader(f"{artist} — {title}")
st.divider()

st.subheader("1. Musical Feature Dynamics")
st.pyplot(fig1)
st.markdown(
    """
    **What this shows:**  
    This plot tracks core musical features over time — including **energy**,
    **spectral change**, and **fatigue**.

    **How to interpret it:**  
    - Sustained high fatigue with low variation may indicate repetition.
    - Sudden spikes in spectral change can signal abrupt transitions.
    - Flat energy curves over long segments often correlate with listener drop-off.

    **Why it matters:**  
    These features form the *input signals* that drive the listener simulation model.
    They explain *why* certain parts of the song are perceived as engaging or tiring.
    """)
st.divider()

st.subheader("2. Listener Disengagement Risk Curve")
st.pyplot(fig2)
st.markdown(
    """
    **What this shows:**  
    A continuous **skip-risk curve** estimating the probability of listener disengagement
    at each moment in the track.

    **How to interpret it:**  
    - Higher values indicate segments where simulated listeners are most likely to exit.
    - Gradual rises often reflect fatigue accumulation.
    - Sharp peaks typically align with structural or textural issues.

    **Why it matters:**  
    This curve converts complex musical behavior into a **single interpretable signal**
    that producers can directly act on — ideal for identifying sections to revise,
    shorten, or restructure.
    """)
st.divider()

st.subheader("3. Engagement State Heatmap")
st.pyplot(fig3)
st.markdown(
    """
    **What this shows:**  
    A heatmap of inferred **listener engagement states** across the song timeline,
    aggregated from thousands of simulated listening sessions.

    **How to interpret it:**  
    - Brighter regions indicate stronger engagement.
    - Darker regions represent higher disengagement probability.
    - Persistent dark bands often align with chorus fatigue or over-extended sections.

    **Why it matters:**  
    Unlike a simple waveform or loudness plot, this visualization reveals **perceptual
    attention patterns**, helping producers understand *where* listeners mentally tune out.
    """
)
st.divider()

st.markdown(
    """
    ### Key Takeaway
    Listener disengagement is rarely caused by a single flaw.  
    It emerges from **feature interactions over time** — repetition, fatigue,
    and abrupt transitions working together.

    This analysis provides **data-driven guidance** to support creative decisions,
    not replace them.
    """
)
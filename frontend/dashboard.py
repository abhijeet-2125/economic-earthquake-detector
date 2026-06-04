import streamlit as st
import requests
import pandas as pd

from components.metrics import metric_card
from components.charts import (
    create_eei_chart,
    create_risk_gauge
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Economic Earthquake Detector",
    layout="wide"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

with open("frontend/assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    """
    <h1 class="main-title">
        Economic Earthquake Detector
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="sub-title">
        Global Systemic Risk Intelligence Platform
    </p>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# API CALLS
# --------------------------------------------------

latest = requests.get(
    "http://127.0.0.1:8000/eei/latest"
).json()

history = requests.get(
    "http://127.0.0.1:8000/eei/chart-data"
).json()

crisis = requests.get(
    "http://127.0.0.1:8000/eei/crisis-days"
).json()

history_df = pd.DataFrame(history)
crisis_df = pd.DataFrame(crisis)

EVENTS = {
    "2020-03-12": "COVID Crash",
    "2020-03-16": "Pandemic Panic",
    "2020-04-20": "Historic Oil Crash",
    "2022-06-13": "Inflation Shock",
    "2021-11-26": "Omicron Fear",
    "2019-08-14": "China Slowdown Fears",
    "2018-02-05": "Volatility Crash",
    "2020-02-24": "COVID Market Selloff"
}

crisis_df["event"] = crisis_df["date"].map(EVENTS)

crisis_df["event"] = crisis_df["event"].fillna(
    "Systemic Risk Event"
)

# --------------------------------------------------
# METRIC CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "EEI",
        round(latest["economic_earthquake_index"], 2)
    )

with col2:
    metric_card(
        "Risk",
        latest["risk_level"]
    )

with col3:
    metric_card(
        "CACI",
        latest["cross_asset_contagion_index"]
    )

with col4:
    metric_card(
        "FTSI",
        round(latest["flight_to_safety_index"], 3)
    )

# --------------------------------------------------
# MAIN DASHBOARD SECTION
# --------------------------------------------------

st.markdown("---")

left, right = st.columns([3, 1])

# ----------------------------
# EEI TIMELINE
# ----------------------------

with left:

    eei_chart = create_eei_chart(
        history_df,
        crisis_df
    )

    st.plotly_chart(
        eei_chart,
        use_container_width=True
    )

# ----------------------------
# RISK GAUGE
# ----------------------------

with right:

    risk_gauge = create_risk_gauge(
        latest["economic_earthquake_index"]
    )

    st.plotly_chart(
        risk_gauge,
        use_container_width=True
    )

# --------------------------------------------------
# TOP CRISIS EVENTS
# --------------------------------------------------

st.markdown("---")

st.subheader("Top Crisis Events")

top_crisis = (
    crisis_df
    .sort_values(
        "economic_earthquake_index",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_crisis[
        [
            "event",
            "date",
            "economic_earthquake_index",
            "risk_level"
        ]
    ],
    use_container_width=True
)
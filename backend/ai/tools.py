from langchain.tools import tool
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine
from backend.database.database import engine

@tool
def get_latest_eei():
    """
    Returns the latest Economic Earthquake Index,
    risk level, contagion score and flight-to-safety score.
    Use when user asks about current risk.
    """

    query = """
    SELECT *
    FROM eei_daily
    ORDER BY date DESC
    LIMIT 1
    """

    df=pd.read_sql(text(query),engine)
    row=df.iloc[0]
    return (
        f"EEI: {row['economic_earthquake_index']}, "
        f"Risk: {row['risk_level']}, "
        f"CACI: {row['cross_asset_contagion_index']}, "
        f"FTSI: {row['flight_to_safety_index']}"
    )

@tool
def get_latest_forecast():
    """
    Returns tomorrow's forecasted Economic Earthquake Index.
    Use when user asks about future risk.
    """

    query = """
    SELECT *
    FROM eei_forecasts
    ORDER BY date DESC
    LIMIT 1
    """
    df=pd.read_sql(text(query),engine)
    row=df.iloc[0]
    return (
        f"Forecasted EEI: "
        f"{row['prediction']}"
    )

@tool
def get_top_anomalies():
    """
    Returns the most severe historical market crises
    detected by the system.
    Use when ask for historical comparison.
    """

    query = """
    SELECT
        date,
        economic_earthquake_index,
        risk_level
    FROM eei_anomalies
    WHERE anomaly = -1
    ORDER BY anomaly_score
    LIMIT 10
    """

    df=pd.read_sql(text(query),engine)
    return df.to_string(index=False)
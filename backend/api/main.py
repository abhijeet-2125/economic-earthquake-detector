from fastapi import FastAPI
import pandas as pd
from sqlalchemy import text
import sys
from pathlib import Path
from backend.ai.economic_analyst import ask_analyst

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.database.database import engine
app = FastAPI(title="Economic Earthquake Detector")

@app.get("/")
def home():
    return {"message": "Economic Earthquake Detector API"}

@app.get("/eei/latest")
def latest_eei():
    query = """
    SELECT *
    FROM eei_daily
    ORDER BY date DESC
    LIMIT 1
    """

    df = pd.read_sql(text(query),engine)
    return df.to_dict(orient="records")[0]

@app.get("/eei/history")
def eei_history(limit: int = 1000):

    query = f"""
    SELECT *
    FROM eei_daily
    ORDER BY date DESC
    LIMIT {limit}
    """

    df = pd.read_sql(text(query),engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")


@app.get("/eei/crisis-days")
def crisis_days():

    query = """
    SELECT *
    FROM eei_daily
    WHERE risk_level = 'CRISIS'
    ORDER BY economic_earthquake_index DESC
    """

    df = pd.read_sql(text(query),engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")

@app.get("/eei/chart-data")
def chart_data():

    query = """
    SELECT
        date,
        economic_earthquake_index,
        risk_level
    FROM eei_daily
    ORDER BY date
    """

    df = pd.read_sql(text(query), engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")

@app.get("/forecast/latest")
def latest_forecast():

    query = """
    SELECT *
    FROM eei_forecasts
    ORDER BY date DESC
    LIMIT 1
    """

    df = pd.read_sql(text(query), engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")[0]


@app.get("/forecast/history")
def forecast_history(limit: int = 100):

    query = f"""
    SELECT *
    FROM eei_forecasts
    ORDER BY date DESC
    LIMIT {limit}
    """

    df = pd.read_sql(text(query), engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")


@app.get("/anomalies/top")
def top_anomalies():
    query = """
    SELECT *
    FROM eei_anomalies
    WHERE anomaly = -1
    ORDER BY anomaly_score
    LIMIT 20
    """

    df = pd.read_sql(text(query),engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict( orient="records")

@app.get("/analyst/chat")
def analyst_chat(question: str):
    answer = ask_analyst(question)

    return {
        "question": question,
        "answer": answer
    }
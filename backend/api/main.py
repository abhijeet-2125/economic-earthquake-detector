from fastapi import FastAPI
import pandas as pd
from sqlalchemy import text
import sys
from pathlib import Path

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

    df = pd.read_sql(
        text(query),
        engine
    )

    df["date"] = df["date"].astype(str)

    return df.to_dict(
        orient="records"
    )


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

    df = pd.read_sql(
        text(query),
        engine
    )

    df["date"] = df["date"].astype(str)

    return df.to_dict(
        orient="records"
    )
import pandas as pd
from sqlalchemy import text
from sklearn.ensemble import IsolationForest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.database.database import engine

#loading data
print("Loading EEI data...")
query = """
SELECT *
FROM eei_daily
ORDER BY date
"""
df = pd.read_sql(text(query),engine)
print("\nShape:")
print(df.shape)

#features for anomaly detection
features = df[
    [
        "economic_earthquake_index",
        "cross_asset_contagion_index",
        "flight_to_safety_index",
        "volatility_shock"
    ]]

#training isolation forest
print("\nTraining Isolation Forest...")
model = IsolationForest(contamination=0.01,n_estimators=300,random_state=42)
df["anomaly"] = model.fit_predict(features)
df["anomaly_score"] = model.decision_function(features)

#saving results
anomaly_results = df[
    [
        "date",
        "economic_earthquake_index",
        "risk_level",
        "anomaly",
        "anomaly_score"
    ]]

anomaly_results.to_sql("eei_anomalies",engine,if_exists="replace",index=False)
print("\nAnomaly table saved successfully!")

#prrinting top anomalies
anomalies = (df[df["anomaly"] == -1].sort_values("anomaly_score"))

print("\nTop 50 Anomalies:")
print(anomalies[[
            "date",
            "economic_earthquake_index",
            "risk_level",
            "anomaly_score"
        ]].head(50))

#oil crash investigation
oil_day = df[df["date"] == "2020-04-20"]
print("\nOil Crash Investigation:")
print(oil_day[[
            "date",
            "economic_earthquake_index",
            "risk_level",
            "anomaly",
            "anomaly_score"
        ]])

print("\nAnomaly Summary:")
print(df["anomaly"].value_counts().rename({
        -1: "Anomaly",
         1: "Normal"
    }))
print("\nDone!")
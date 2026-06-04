import pandas as pd
from sqlalchemy import text
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.database.database import engine

print("Loading EEI data...")
query = """
SELECT *
FROM eei_daily
ORDER BY date
"""
df = pd.read_sql(text(query),engine)

#creating lag features
df["lag_1"] = df["economic_earthquake_index"].shift(1)
df["lag_3"] = df["economic_earthquake_index"].shift(3)
df["lag_7"] = df["economic_earthquake_index"].shift(7)
df["lag_14"] = df["economic_earthquake_index"].shift(14)
df = df.dropna()

#splitting data into train and test
split_index = int(len(df) * 0.8)
train = df.iloc[:split_index]
test = df.iloc[split_index:]
X_train = train[["lag_1", "lag_3", "lag_7", "lag_14"]]
y_train = train["economic_earthquake_index"]
X_test = test[["lag_1", "lag_3", "lag_7", "lag_14"]]
y_test = test["economic_earthquake_index"]

#training the model for forecasting
print("Training XGBoost...")
model = XGBRegressor(n_estimators=300,max_depth=4,learning_rate=0.05,random_state=42)
model.fit(X_train, y_train)

#prediction and evaluation
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test,predictions) ** 0.5

print("\nForecast Metrics:")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")

#Next day forecasting 
latest = df.iloc[-1]
future_input = pd.DataFrame({
    "lag_1": [latest["economic_earthquake_index"]],
    "lag_3": [df.iloc[-3]["economic_earthquake_index"]],
    "lag_7": [df.iloc[-7]["economic_earthquake_index"]],
    "lag_14": [df.iloc[-14]["economic_earthquake_index"]]})

forecast = model.predict(future_input)[0]
print("\nTomorrow EEI Forecast:")
print(round(float(forecast), 4))

test = test.copy()
test["prediction"] = predictions
forecast_results = test[[
        "date",
        "economic_earthquake_index",
        "prediction"]]

forecast_results.to_sql("eei_forecasts",engine,if_exists="replace",index=False)
print("\nForecast table saved successfully")
print(f"Rows Saved: {len(forecast_results)}")
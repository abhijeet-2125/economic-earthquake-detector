import pandas as pd
from database import engine

print("\nReading financial data...")

df = pd.read_csv("backend/data/financial_data.csv")
df.columns = ["date","ticker","open","high","low","close","volume"]

print(f"\nRows found: {len(df)}")
print("\nColumns:")
print(df.columns.tolist())
print("\nLoading data into PostgreSQL...")

try:
    df.to_sql("market_data",engine,if_exists="append",index=False)
    print("\nData loaded successfully!")
except Exception as e:
    print("\nError:")
    print(e)
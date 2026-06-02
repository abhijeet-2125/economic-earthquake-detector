import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from backend.database.database import engine

print("Reading economic data...")

df = pd.read_csv("backend/economic/economic_data.csv")

print(f"Rows found: {len(df)}")
print("Loading into PostgreSQL...")
df.to_sql("economic_data",engine,if_exists="append",index=False)
print("Economic data loaded successfully!")
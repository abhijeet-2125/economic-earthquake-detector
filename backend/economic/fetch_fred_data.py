from fredapi import Fred
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
fred=Fred(api_key=os.getenv("FRED_API_KEY"))

indicators = {"CPI": "CPIAUCSL","UNEMPLOYMENT": "UNRATE","FED_FUNDS": "FEDFUNDS", "GDP": "GDP", "RECESSION": "USREC"}
all_data=[]
for name,code in indicators.items():
    print(f"Downloading {name}...")
    series = fred.get_series(code)
    temp_df = pd.DataFrame({"date":series.index,"indicator":name,"value":series.values})
    all_data.append(temp_df)

final_df = pd.concat(all_data,ignore_index=True)

print("\nShape:")
print(final_df.shape)

print("\nSample:")
print(final_df.head())
final_df.to_csv("backend/economic/economic_data.csv",index=False)
print("\nSaved successfully!")
import yfinance as yf
import pandas as pd
from pathlib import Path



TICKERS = [
    "^GSPC",      # S&P 500
    "^VIX",       # Volatility Index
    "^TNX",       # US Treasury 
    "GC=F",       # Gold
    "CL=F",       # Crude Oil
    "EURUSD=X",   # Euro/USD
    "JPY=X",      # Japanese Yen
    "BTC-USD",    # Bitcoin
    "ETH-USD",    # Ethereum
    "TLT",        # Long-Term Bonds
    "SOXX",       # Semiconductor ETF
    "EEM"         # Emerging Markets ETF
]

DATA_DIR = Path("backend/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "financial_data.csv"
all_data = []

print("\nStarting data collection...\n")
for ticker in TICKERS:
    try:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker,period="10y",auto_adjust=True,progress=False)
        if df.empty:
            print(f"⚠ No data returned for {ticker}")
            continue

        #to handle multi-level columns as it is giving error when am trying to reset index
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns.name = None
        df.reset_index(inplace=True)
        df["Ticker"] = ticker
        all_data.append(df)
        print(f"✓ {ticker}: {len(df)} rows")
    except Exception as e:
        print(f"✗ Error downloading {ticker}: {e}")



final_df = pd.concat(all_data,ignore_index=True) 
final_df = final_df[["Date","Ticker", "Open","High","Low","Close","Volume"]]

#data quality report
print("DATA QUALITY REPORT")

print("\nShape:")
print(final_df.shape)

print("\nMissing Values:")
print(final_df.isnull().sum())

print("\nUnique Assets:")
print(final_df["Ticker"].nunique())

print("\nAssets:")
print(final_df["Ticker"].unique())

print("\nDate Range:")
print(final_df["Date"].min(),"to",final_df["Date"].max())

#saving data to csv
final_df.to_csv(OUTPUT_FILE,index=False)
print(f"\nFile Location: {OUTPUT_FILE}")
print("\nSample Data:")
print(final_df.head())
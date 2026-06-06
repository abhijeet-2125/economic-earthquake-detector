import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import pandas as pd
from sqlalchemy import text
from backend.database.database import engine


query = """SELECT * FROM market_data"""

df = pd.read_sql(text(query),engine)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["ticker", "date"])

print("Generating features.....")
feature_dfs = []
for ticker, group in df.groupby("ticker"):
    group = group.copy()

    # Daily Return
    group["daily_return"] = (group["close"].pct_change())
    group["log_return"] = np.where((group["close"] > 0) &(group["close"].shift(1) > 0),np.log(
        group["close"] /
        group["close"].shift(1)
    ),
    np.nan)

    # EMA
    group["ema_7"] = (group["close"].ewm(span=7, adjust=False).mean())
    group["ema_30"] = (group["close"].ewm(span=30, adjust=False).mean())
    group["ema_90"] = (group["close"].ewm(span=90, adjust=False).mean())

    # Rolling Volatility
    group["rolling_volatility_30"] = (group["daily_return"].rolling(30).std())

    # Drawdown
    rolling_peak = (group["close"].cummax())
    group["drawdown"] = ((group["close"] - rolling_peak)/rolling_peak)

    #volatility shock
    group["volatility_shock"] = (group["rolling_volatility_30"]-group["rolling_volatility_30"].ewm(span=90, adjust=False).mean())

    #Momentum spread
    group["momentum_spread"] = (group["ema_7"]-group["ema_90"]) / group["ema_90"]

    #PER ASSET STREss
    group["asset_stress_score"] = (abs(group["daily_return"])+group["rolling_volatility_30"].fillna(0)+abs(group["drawdown"]))
    feature_dfs.append(group)

features_df = pd.concat(feature_dfs,ignore_index=True)

#CROSS-ASSET CONTAGION INDEX (CACI)
features_df["abnormal_move"] = (abs(features_df["daily_return"]) >2 * features_df["rolling_volatility_30"])
caci_assets = features_df[features_df["ticker"] != "^VIX"]
caci = (caci_assets.groupby("date")["abnormal_move"].sum().reset_index()) 
caci.columns = ["date","cross_asset_contagion_index"]
features_df = features_df.merge(caci,on="date",how="left")


# FLIGHT TO SAFETY INDEX (FTSI)
returns_pivot = features_df.pivot(index="date",columns="ticker",values="daily_return")
ftsi = pd.DataFrame(index=returns_pivot.index)
ftsi["flight_to_safety_index"] = (
    returns_pivot["GC=F"].fillna(0) +      # Gold
    returns_pivot["TLT"].fillna(0) +       # Bonds
    returns_pivot["JPY=X"].fillna(0)       # Yen
    -
    returns_pivot["^GSPC"].fillna(0)       # Stocks
    -
    returns_pivot["BTC-USD"].fillna(0)     # Bitcoin
    -
    returns_pivot["ETH-USD"].fillna(0)     # Ethereum
)

ftsi.reset_index(inplace=True)
features_df = features_df.merge(ftsi,on="date",how="left")

#Economic earthquake index
# DAILY FEATURE AGGREGATION
daily_features = (features_df.groupby("date")
    .agg(
        {
            "cross_asset_contagion_index": "first",
            "flight_to_safety_index": "first",
            "volatility_shock": "mean"
        }
    )
    .reset_index())
print("\nDaily Features Shape:")
print(daily_features.shape)

# =====================================
# ECONOMIC EARTHQUAKE INDEX (EEI)
# =====================================
from scipy.stats import zscore
daily_features["caci_z"] = zscore(daily_features["cross_asset_contagion_index"])
daily_features["ftsi_z"] = zscore(daily_features["flight_to_safety_index"])
daily_features["volshock_z"] = zscore(daily_features["volatility_shock"].fillna(0))
daily_features["economic_earthquake_index"] = (
    0.4 * daily_features["caci_z"]
    +
    0.4 * daily_features["ftsi_z"]
    +
    0.2 * daily_features["volshock_z"])


def classify_risk(eei):  #classifying the risk
    if eei >= 3:
        return "CRISIS"
    elif eei >= 2:
        return "HIGH"
    elif eei >= 1:
        return "ELEVATED"
    else:
        return "NORMAL"
daily_features["risk_level"] = (daily_features["economic_earthquake_index"].apply(classify_risk))
daily_features[
    [
        "date",
        "cross_asset_contagion_index",
        "flight_to_safety_index",
        "volatility_shock",
        "economic_earthquake_index",
        "risk_level"
    ]].to_sql("eei_daily",engine,if_exists="replace", index=False)
print("\nEEI Table Created Successfully")


print("\nGenerated Features:")
print(features_df[
        [
            "ticker",
            "date",
            "daily_return",
            "ema_7",
            "ema_30",
            "ema_90",
            "rolling_volatility_30",
            "drawdown"
        ]
    ].head())

print("\nShape:")
print(features_df.shape)

#validating the features
print("\nMissing Values:")
print(features_df[
        [
            "daily_return",
            "ema_7",
            "ema_30",
            "ema_90",
            "rolling_volatility_30",
            "drawdown"
        ]
    ].isnull().sum()
)

print("\nSummary Statistics:")
print(
    features_df[
        [
            "daily_return",
            "rolling_volatility_30",
            "drawdown"
        ]
    ].describe()
)
#got -305% which is impossible so there is some error in the code and need to find it out
extreme_returns = features_df[
    features_df["daily_return"] < -1
]

print(extreme_returns[
    ["ticker", "date", "close", "daily_return"]
].head(20))

#damn so its just a real historical event:2020 Oil Price Crash
#On 20 April 2020, WTI crude oil futures went negative for the first time in history because storage facilities were full during the COVID demand collapse.

features_df[["id","date","ticker", "daily_return","ema_7","ema_30","ema_90", "rolling_volatility_30","drawdown","volatility_shock","momentum_spread","asset_stress_score","cross_asset_contagion_index"]].to_sql("market_features",engine,if_exists="replace",index=False)
print("\nFeature Store Created Successfully!")

#validating the stored features
print(features_df[["log_return","volatility_shock","momentum_spread","asset_stress_score"]].describe())


print("\nCACI Summary:")
print(features_df["cross_asset_contagion_index"].describe())


#trying to find the days with highest cross-asset contagion index
top_caci_days = (caci.sort_values("cross_asset_contagion_index",ascending=False).head(20))
print(top_caci_days)

#when i searched i not found any major event on 17-05-2017 , which has highest caci, but it could be due to some specific asset which had an extreme move on that day, so i will check the features_df for that date
investigation = features_df[
    features_df["date"] == "2017-05-17"
][
    [
        "ticker",
        "daily_return",
        "rolling_volatility_30",
        "abnormal_move"
    ]
].sort_values(
    "daily_return"
)

print("\nInvestigation:")
print(investigation)

print("\nFTSI Summary:")
print(
    features_df[
        "flight_to_safety_index"
    ].describe()
)

print("\nEEI Summary:")
print(daily_features[ "economic_earthquake_index" ].describe())
print("\nTop 20 EEI Days:")
print(daily_features.sort_values("economic_earthquake_index",ascending=False).head(20))

print("\nRisk Level Counts:")
print(daily_features["risk_level"].value_counts())


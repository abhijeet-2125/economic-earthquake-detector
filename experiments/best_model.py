#importing the dependencies
!pip install catboost
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score

#loading the datasets
train = pd.read_csv("/content/extracted_data/dataset/train.csv")
test = pd.read_csv("/content/extracted_data/dataset/test.csv")

#feature engineering as by the eda sugestions
def create_features(df):
    df = df.copy()
    df["hour"] = df["timestamp"].str.split(":").str[0].astype(int)
    df["minute"] = df["timestamp"].str.split(":").str[1].astype(int)
    df["temp_missing"] = df["Temperature"].isnull().astype(int)
    df["weather_missing"] = df["Weather"].isnull().astype(int)
    df["road_missing"] = df["RoadType"].isnull().astype(int)
    return df


train = create_features(train)
test = create_features(test)

#missing values imputation
train["RoadType"] = train["RoadType"].fillna("Unknown")
test["RoadType"] = test["RoadType"].fillna("Unknown")
train["Weather"] = train["Weather"].fillna("Unknown")
test["Weather"] = test["Weather"].fillna("Unknown")
temp_median = train["Temperature"].median()

train["Temperature"] = train["Temperature"].fillna(temp_median)
test["Temperature"] = test["Temperature"].fillna(temp_median)
geo_freq = train["geohash"].value_counts()

train["geohash_freq"] = train["geohash"].map(geo_freq)
test["geohash_freq"] = test["geohash"].map(geo_freq)
test["geohash_freq"] = test["geohash_freq"].fillna(0)


train["RoadType_Hour"] = (
    train["RoadType"].astype(str)
    + "_"
    + train["hour"].astype(str)
)

test["RoadType_Hour"] = (
    test["RoadType"].astype(str)
    + "_"
    + test["hour"].astype(str)
)

train["RoadType_Lanes"] = (
    train["RoadType"].astype(str)
    + "_"
    + train["NumberofLanes"].astype(str)
)

test["RoadType_Lanes"] = (
    test["RoadType"].astype(str)
    + "_"
    + test["NumberofLanes"].astype(str)
)


#decided features and target
TARGET = "demand"
FEATURES = [

    "geohash",
    "day",
    "RoadType",
    "RoadType_Hour",
    "RoadType_Lanes",
    "NumberofLanes",
    "LargeVehicles",
    "Landmarks",
    "Weather",
    "Temperature",
    "hour",
    "minute",
    "geohash_freq",
    "temp_missing",
    "weather_missing",
    "road_missing"
]

CAT_FEATURES = [
    "geohash",
    "RoadType",
    "RoadType_Hour",
    "RoadType_Lanes",
    "LargeVehicles",
    "Landmarks",
    "Weather"
]


X = train[FEATURES]
y = train[TARGET]
X_test = test[FEATURES]

#calcutaing the cv
kf = KFold(n_splits=5, shuffle=True,random_state=42)
oof = np.zeros(len(train))
test_preds = np.zeros(len(test))
feature_importances = []

#training
for fold, (tr_idx, val_idx) in enumerate(kf.split(X)):
    print(f"\n========== FOLD {fold+1} ==========")

    X_train = X.iloc[tr_idx]
    y_train = y.iloc[tr_idx]
    X_val = X.iloc[val_idx]
    y_val = y.iloc[val_idx]

    model = CatBoostRegressor(
        iterations=5000,
        learning_rate=0.03,
        depth=8,
        l2_leaf_reg=5,
        loss_function="RMSE",
        eval_metric="R2",
        random_seed=42,
        verbose=200,
        early_stopping_rounds=300)

    model.fit(
        X_train,
        y_train,
        cat_features=CAT_FEATURES,
        eval_set=(X_val, y_val),
        use_best_model=True)

    preds = model.predict(X_val)
    oof[val_idx] = preds
    fold_r2 = r2_score(y_val, preds)
    print(f"Fold R2 = {fold_r2:.6f}")
    test_preds += model.predict(X_test) / 5
    feature_importances.append(model.get_feature_importance())



cv_r2 = r2_score(y, oof)
print("\n======================")
print("FINAL CV R2")
print("======================")
print(cv_r2)
print("\nCompetition Score Estimate")
print(max(0, 100 * cv_r2))

#feature importance
importance = pd.DataFrame({"feature": FEATURES, "importance":np.mean(feature_importances, axis=0)})
importance = importance.sort_values("importance",ascending=False)

print("\n======================")
print("FEATURE IMPORTANCE")
print("======================")

print(importance)
submission = pd.DataFrame({"Index": test["Index"],"demand": test_preds})
submission.to_csv("submission_catboost_v1.csv",index=False)
print("\nsubmission_catboost_v1.csv saved")
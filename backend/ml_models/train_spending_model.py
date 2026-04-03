import os
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from prophet import Prophet

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "financial_hci_dataset.csv") # Transactions
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("Loading transactions dataset for Spending Prediction...")
df = pd.read_csv(DATA_PATH)

# For XGBoost we can try predicting Budget_Utilized based on other static features or aggregated features over time
# For Prophet, we need 'ds' (date) and 'y' (amount)

# 1. Train XGBoost
print("Training XGBoost...")
features = ['Amount', 'Credit_Score'] # In real app we would use historic aggregations
target = 'Budget_Utilized'

if target in df.columns:
    X_xgb = df[features].fillna(0)
    y_xgb = df[target].fillna(0)
    
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_xgb, y_xgb)
    
    xgb_path = os.path.join(MODEL_DIR, "spending_xgboost.pkl")
    joblib.dump(xgb_model, xgb_path)
    print(f"XGBoost Model saved successfully at {xgb_path}")
else:
    print(f"Target '{target}' not found for XGBoost.")

# 2. Train Prophet
print("Training Prophet Model...")
if 'Date' in df.columns and 'Amount' in df.columns:
    prophet_df = df[['Date', 'Amount']].rename(columns={'Date': 'ds', 'Amount': 'y'})
    # Group by date to get total daily spend
    prophet_df = prophet_df.groupby('ds', as_index=False).sum()
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds'], format="%Y-%m-%d")
    
    prophet_model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    prophet_model.fit(prophet_df)
    
    prophet_path = os.path.join(MODEL_DIR, "spending_prophet.json")
    # Prophet provides built-in JSON serialization. Using joblib works too but saving to json is better
    from prophet.serialize import model_to_json
    with open(prophet_path, 'w') as fout:
        fout.write(model_to_json(prophet_model))
    print(f"Prophet Model saved successfully at {prophet_path}")
else:
    print("Required columns for Prophet not found.")

import os
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from prophet import Prophet
from prophet.serialize import model_to_json
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "processed", "financial_profiles.csv")
TRANS_PATH = os.path.join(BASE_DIR, "data", "raw", "financial_hci_dataset.csv") 
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# ---------------------------------------------------------
# PHASE 2.1: Train XGBoost (Behavior Model) using Dataset A
# ---------------------------------------------------------
print("Loading snapshot dataset for XGBoost Behavior Modeling...")
df_prof = pd.read_csv(PROFILE_PATH)

# Feature engineering (Ratios)
df_prof['expense_ratio'] = df_prof['monthly_expenses'] / df_prof['monthly_income'].replace(0, 1)
df_prof['debt_ratio'] = df_prof['loan_amount'] / (df_prof['monthly_income'] * 12).replace(0, 1)

# Ensure budget_stability is explicitly generated accurately relative to the engineered proportion.
df_prof["budget_stability"] = 1 - df_prof["expense_ratio"]
df_prof["budget_stability"] = df_prof["budget_stability"].clip(0, 1)

features = [
    "monthly_income",
    "monthly_expenses",
    "total_savings",
    "credit_score",
    "expense_ratio",
    "debt_ratio"
]
target = "budget_stability"

X_xgb = df_prof[features].fillna(0)
y_xgb = df_prof[target].fillna(0)

# Scale features to assist XGBoost trees
scaler = StandardScaler()
X_xgb_scaled = scaler.fit_transform(X_xgb)
joblib.dump(scaler, os.path.join(MODEL_DIR, "spending_xgb_scaler.pkl"))

print("Training XGBoost...")
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb_model.fit(X_xgb_scaled, y_xgb)

xgb_path = os.path.join(MODEL_DIR, "spending_xgboost.pkl")
joblib.dump(xgb_model, xgb_path)
print(f"XGBoost Behavior Model saved successfully at {xgb_path}")

# ---------------------------------------------------------
# PHASE 2.2: Train Prophet (Temporal Model) using Dataset B
# ---------------------------------------------------------
print("Loading transactions dataset for Prophet Temporal Modeling...")
df_trans = pd.read_csv(TRANS_PATH)

# We want out-flowing transactions -> Expenses
df_exp = df_trans[df_trans['Transaction_Type'] == 'Expense'].copy()

# Group by Date
df_daily = df_exp.groupby("Date")["Amount"].sum().reset_index()
df_daily.columns = ['ds', 'y']
# Mandatory formatting for Prophet internal bayesian logic
df_daily['ds'] = pd.to_datetime(df_daily['ds'])

print("Training Prophet...")
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(df_daily)

# Prophet serialized via JSON instead of joblib natively
with open(os.path.join(MODEL_DIR, "spending_prophet.json"), 'w') as fout:
    fout.write(model_to_json(model))
print("Prophet Temporal forecast saved successfully!")

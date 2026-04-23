import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "financial_hci_dataset.csv") # Transactions
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("Loading transactions dataset for Anomaly Detection...")
df = pd.read_csv(DATA_PATH)

# Feature engineering for anomaly detection
df['transaction_impact'] = df['Amount'] / np.maximum(df['Balance_After_Transaction'], 1)

features = ['Amount'] # Adding more features if available, like Balance_After_Transaction
if 'Balance_After_Transaction' in df.columns:
    features.append('Balance_After_Transaction')
features.append('transaction_impact')

X = df[features].fillna(0)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, os.path.join(MODEL_DIR, "anomaly_scaler.pkl"))

# 1. Train Isolation Forest
print("Training Isolation Forest...")
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X_scaled)

# Save Isolation Forest
iso_model_path = os.path.join(MODEL_DIR, "isolation_forest.pkl")
joblib.dump(iso_forest, iso_model_path)
print(f"Isolation Forest saved successfully at {iso_model_path}")


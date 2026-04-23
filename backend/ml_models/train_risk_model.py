import os
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "financial_profiles.csv")
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("Loading dataset for Risk Model...")
df = pd.read_csv(DATA_PATH)

# Feature Engineering
df['expense_ratio'] = df['monthly_expenses'] / df['monthly_income'].replace(0, 1)
df['debt_ratio'] = df['loan_amount'] / (df['monthly_income'] * 12).replace(0, 1)

features = ['age', 'monthly_income', 'monthly_expenses', 'total_savings', 
            'loan_amount', 'monthly_emi', 'credit_score', 'credit_card_usage',
            'expense_ratio', 'debt_ratio']
X = df[features]
y = df['risk_level'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, os.path.join(MODEL_DIR, "risk_scaler.pkl"))

# Build XGBoost Model
print("Building and training Risk Prediction Model (XGBoost)...")
model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)

# Train Model
model.fit(X_train_scaled, y_train)

# Evaluate Model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Risk Model Test Accuracy: {accuracy:.4f}")

# Save Model
model_save_path = os.path.join(MODEL_DIR, "risk_model.pkl")
joblib.dump(model, model_save_path)
print(f"Risk Model saved successfully at {model_save_path}")

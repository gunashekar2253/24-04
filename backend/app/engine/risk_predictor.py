"""
Risk Predictor Engine
Loads the trained XGBoost model and scaler to predict financial risk.
"""
import os
import numpy as np
import joblib
from app.config import settings


class RiskPredictor:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.model = joblib.load(os.path.join(base, settings.RISK_MODEL_PATH))
        self.scaler = joblib.load(os.path.join(base, settings.RISK_SCALER_PATH))

    def predict(self, profile: dict) -> dict:
        """
        Accepts a dict with keys:
          age, monthly_income, monthly_expenses, total_savings,
          loan_amount, monthly_emi, credit_score, credit_card_usage
        Returns risk score and label.
        """
        income = max(profile["monthly_income"], 1)
        expense_ratio = profile["monthly_expenses"] / income
        debt_ratio = profile["loan_amount"] / (income * 12)

        features = np.array([[ 
            profile["age"],
            profile["monthly_income"],
            profile["monthly_expenses"],
            profile["total_savings"],
            profile["loan_amount"],
            profile["monthly_emi"],
            profile["credit_score"],
            profile["credit_card_usage"],
            expense_ratio,
            debt_ratio
        ]])

        scaled = self.scaler.transform(features)
        prob = float(self.model.predict_proba(scaled)[0][1])

        # --- FINANCIAL HEURISTIC OVERLAY ---
        # XGBoost trees can fail on extreme monetary outliers (e.g. 150k income)
        # by routing them to "rich bounds" and ignoring equally extreme expenses.

        if expense_ratio > 0.95:
            prob = max(prob, 0.88)
        elif expense_ratio > 0.80:
            prob = max(prob, 0.65)
            
        if debt_ratio > 3.0:
            prob = max(prob, 0.85)
        elif debt_ratio > 1.5:
            prob = max(prob, 0.55)

        if profile["credit_score"] < 500:
            prob = max(prob, 0.80)

        prob = min(prob, 0.99)
        # --- END OVERLAY ---

        if prob >= 0.7:
            label = "High Risk"
        elif prob >= 0.4:
            label = "Medium Risk"
        else:
            label = "Low Risk"

        return {
            "risk_score": round(prob * 100, 2),
            "risk_label": label,
            "details": {
                "default_probability": round(prob, 4),
                "credit_score_input": profile["credit_score"],
                "debt_to_income": round(profile["monthly_emi"] / (profile["monthly_income"] + 1), 4),
            }
        }


# Singleton instance
risk_predictor = RiskPredictor()


# import os
# import pandas as pd
# import numpy as np
# import joblib

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import accuracy_score

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.utils import to_categorical

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "financial_profiles.csv")
# MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

# if not os.path.exists(MODEL_DIR):
#     os.makedirs(MODEL_DIR)

# print("Loading dataset for Risk Model (Deep Learning)...")
# df = pd.read_csv(DATA_PATH)

# # -----------------------------
# # Feature Engineering (same)
# # -----------------------------
# df['expense_ratio'] = df['monthly_expenses'] / df['monthly_income'].replace(0, 1)
# df['debt_ratio'] = df['loan_amount'] / (df['monthly_income'] * 12).replace(0, 1)

# features = [
#     'age', 'monthly_income', 'monthly_expenses', 'total_savings',
#     'loan_amount', 'monthly_emi', 'credit_score', 'credit_card_usage',
#     'expense_ratio', 'debt_ratio'
# ]

# X = df[features]
# y = df['risk_level']   # assume 0,1,2 classes

# # -----------------------------
# # Train-test split
# # -----------------------------
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# # -----------------------------
# # Scaling (same as your code)
# # -----------------------------
# print("Scaling features...")
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# joblib.dump(scaler, os.path.join(MODEL_DIR, "risk_scaler.pkl"))

# # -----------------------------
# # Convert labels (for NN)
# # -----------------------------
# num_classes = len(np.unique(y))
# y_train_cat = to_categorical(y_train, num_classes)
# y_test_cat = to_categorical(y_test, num_classes)

# # -----------------------------
# # Build Neural Network (ReLU)
# # -----------------------------
# print("Building Deep Learning Model...")

# model = Sequential([
#     Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
#     Dense(32, activation='relu'),
#     Dense(16, activation='relu'),
#     Dense(num_classes, activation='softmax')   # classification
# ])

# model.compile(
#     optimizer='adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )

# # -----------------------------
# # Train Model
# # -----------------------------
# print("Training model...")
# model.fit(
#     X_train_scaled,
#     y_train_cat,
#     epochs=30,
#     batch_size=16,
#     validation_split=0.1,
#     verbose=1
# )

# # -----------------------------
# # Evaluate
# # -----------------------------
# print("Evaluating model...")
# loss, acc = model.evaluate(X_test_scaled, y_test_cat)
# print(f"Deep Learning Test Accuracy: {acc:.4f}")

# # -----------------------------
# # Save Model
# # -----------------------------
# model_path = os.path.join(MODEL_DIR, "risk_model_nn.h5")
# model.save(model_path)

# print(f"Deep Learning Model saved at {model_path}")
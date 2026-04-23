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

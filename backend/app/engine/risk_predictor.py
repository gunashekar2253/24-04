"""
Risk Predictor Engine
Loads the trained TensorFlow ReLU model and scaler to predict financial risk.
"""
import os
import numpy as np
import joblib
import tensorflow as tf
from app.config import settings


class RiskPredictor:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.model = tf.keras.models.load_model(os.path.join(base, settings.RISK_MODEL_PATH))
        self.scaler = joblib.load(os.path.join(base, settings.RISK_SCALER_PATH))

    def predict(self, profile: dict) -> dict:
        """
        Accepts a dict with keys:
          age, monthly_income, monthly_expenses, total_savings,
          loan_amount, monthly_emi, credit_score, credit_card_usage
        Returns risk score and label.
        """
        features = np.array([[
            profile["age"],
            profile["monthly_income"],
            profile["monthly_expenses"],
            profile["total_savings"],
            profile["loan_amount"],
            profile["monthly_emi"],
            profile["credit_score"],
            profile["credit_card_usage"]
        ]])
        scaled = self.scaler.transform(features)
        prob = float(self.model.predict(scaled, verbose=0)[0][0])

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

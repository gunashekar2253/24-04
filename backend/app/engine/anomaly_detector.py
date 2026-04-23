"""
Anomaly Detector Engine
Uses Isolation Forest to detect anomalous transactions.
"""
import os
import numpy as np
import joblib
from app.config import settings


class AnomalyDetector:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.scaler = joblib.load(os.path.join(base, settings.ANOMALY_SCALER_PATH))
        self.iso_forest = joblib.load(os.path.join(base, settings.ANOMALY_ISO_PATH))

    def detect(self, amount: float, balance: float) -> dict:
        """
        Check if a single transaction is anomalous.
        Returns anomaly flags from Isolation Forest.
        """
        impact = amount / max(balance, 1)
        features = np.array([[amount, balance, impact]])
        scaled = self.scaler.transform(features)

        # Isolation Forest: -1 = anomaly, 1 = normal
        iso_pred = int(self.iso_forest.predict(scaled)[0])
        score = float(self.iso_forest.decision_function(scaled)[0])
        iso_anomaly = iso_pred == -1

        # Relative Severity Overlay
        severity = "Normal"
        if iso_anomaly:
            if impact > 0.5 or amount > 50000:
                severity = "Critical"
            elif impact > 0.2 or amount > 5000:
                severity = "High"
            elif amount > 500:
                severity = "Medium"
            else:
                # Suppress negligible monetary anomalies
                iso_anomaly = False
                severity = "Normal"

        return {
            "is_anomaly": iso_anomaly,
            "isolation_forest": {
                "prediction": "Anomaly" if iso_anomaly else "Normal",
                "ml_score": score
            },
            "severity": severity
        }

    def detect_batch(self, transactions: list) -> list:
        """Detect anomalies across a list of transactions (each has 'amount' and 'balance')."""
        return [self.detect(t["amount"], t["balance"]) for t in transactions]


# Singleton instance
anomaly_detector = AnomalyDetector()

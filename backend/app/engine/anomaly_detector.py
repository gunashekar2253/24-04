"""
Anomaly Detector Engine
Uses Isolation Forest + Autoencoder to detect anomalous transactions.
"""
import os
import numpy as np
import joblib
import tensorflow as tf
from app.config import settings


class AnomalyDetector:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.scaler = joblib.load(os.path.join(base, settings.ANOMALY_SCALER_PATH))
        self.iso_forest = joblib.load(os.path.join(base, settings.ANOMALY_ISO_PATH))
        self.autoencoder = tf.keras.models.load_model(os.path.join(base, settings.ANOMALY_AE_PATH), compile=False)

    def detect(self, amount: float, balance: float) -> dict:
        """
        Check if a single transaction is anomalous.
        Returns anomaly flags from both Isolation Forest and Autoencoder.
        """
        features = np.array([[amount, balance]])
        scaled = self.scaler.transform(features)

        # Isolation Forest: -1 = anomaly, 1 = normal
        iso_pred = int(self.iso_forest.predict(scaled)[0])
        iso_anomaly = iso_pred == -1

        # Autoencoder: high reconstruction error = anomaly
        reconstructed = self.autoencoder.predict(scaled, verbose=0)
        reconstruction_error = float(np.mean(np.abs(scaled - reconstructed)))
        ae_anomaly = reconstruction_error > 0.5  # Threshold

        is_anomaly = iso_anomaly or ae_anomaly

        return {
            "is_anomaly": is_anomaly,
            "isolation_forest": {
                "prediction": "Anomaly" if iso_anomaly else "Normal",
                "raw_score": iso_pred
            },
            "autoencoder": {
                "prediction": "Anomaly" if ae_anomaly else "Normal",
                "reconstruction_error": round(reconstruction_error, 4)
            },
            "severity": "High" if (iso_anomaly and ae_anomaly) else ("Medium" if is_anomaly else "Low")
        }

    def detect_batch(self, transactions: list) -> list:
        """Detect anomalies across a list of transactions (each has 'amount' and 'balance')."""
        return [self.detect(t["amount"], t["balance"]) for t in transactions]


# Singleton instance
anomaly_detector = AnomalyDetector()

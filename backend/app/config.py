import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Finance AI"
    VERSION: str = "1.0.0"

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./finance.db")

    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # ML Model Paths
    RISK_MODEL_PATH: str = "ml_models/risk_model.h5"
    RISK_SCALER_PATH: str = "ml_models/risk_scaler.pkl"
    ANOMALY_ISO_PATH: str = "ml_models/isolation_forest.pkl"
    ANOMALY_AE_PATH: str = "ml_models/autoencoder.h5"
    ANOMALY_SCALER_PATH: str = "ml_models/anomaly_scaler.pkl"
    SPENDING_XGB_PATH: str = "ml_models/spending_xgboost.pkl"
    SPENDING_PROPHET_PATH: str = "ml_models/spending_prophet.json"

    # Dataset
    DATASET_PATH: str = "data/processed/financial_profiles.csv"


settings = Settings()

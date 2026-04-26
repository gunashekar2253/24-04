"""
Spending Forecaster Engine
Uses XGBoost for explicit Behavioral profiling and Prophet for time-series forecasting.
"""
import os
import json
import numpy as np
import pandas as pd
import joblib
from app.config import settings

# Gracefully import model_from_json
try:
    from prophet.serialize import model_from_json
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


class SpendingForecaster:
    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Load Phase 2.1 XGBoost Behavioral Model
        self.xgb_model = joblib.load(os.path.join(base, settings.SPENDING_XGB_PATH))
        self.xgb_scaler = joblib.load(os.path.join(base, "ml_models", "spending_xgb_scaler.pkl"))
        
        # Load Phase 2.2 Prophet Temporal Model
        prophet_path = os.path.join(base, "ml_models", "spending_prophet.json")
        if os.path.exists(prophet_path) and PROPHET_AVAILABLE:
            with open(prophet_path, 'r') as fin:
                self.prophet_model = model_from_json(fin.read())
        else:
            self.prophet_model = None

    def evaluate_behavior(self, profile_dict: dict) -> float:
        """Phase 3.1 Behavior Evaluation (XGBoost)"""
        income = max(profile_dict.get("monthly_income", 1), 1)
        expenses = profile_dict.get("monthly_expenses", 0)
        savings = profile_dict.get("total_savings", 0)
        credit = profile_dict.get("credit_score", 0)
        loan = profile_dict.get("loan_amount", 0)

        expense_ratio = expenses / income
        debt_ratio = loan / max((income * 12), 1)

        # Match exact features trained: 
        # ["monthly_income", "monthly_expenses", "total_savings", "credit_score", "expense_ratio", "debt_ratio"]
        features = np.array([[income, expenses, savings, credit, expense_ratio, debt_ratio]])
        scaled = self.xgb_scaler.transform(features)
        
        # Predicts budget_stability (our static behavior score) 0.0 - 1.0 (Higher is more stable)
        behavior_score = float(self.xgb_model.predict(scaled)[0])
        return min(max(behavior_score, 0.0), 1.0) # Clamp boundaries

    def get_real_daily_avg(self, transactions: list) -> float:
        if not transactions:
            return 0.0
            
        expenses = [t.amount for t in transactions if t.type == "expense"]
        if not expenses:
            return 0.0
            
        import numpy as np
        # Outlier control
        expenses = np.clip(expenses, 0, np.percentile(expenses, 95)).tolist()
        unique_days = len(set([t.date.strftime("%Y-%m-%d") for t in transactions]))
        return float(sum(expenses) / max(unique_days, 1))

    def forecast_spending(self, days: int = 30, profile_dict: dict = None, transactions: list = None) -> dict:
        """Phase 3.2 Time-Series Forecasting (Prophet) with Blending"""
        if self.prophet_model is None:
            # Fallback logic if Prophet fails
            fallback_spend = profile_dict.get("monthly_expenses", 0) / 30 if profile_dict else 0
            return {"forecast_days": days, "predictions": [], "avg_future_spend": fallback_spend, "trend": 0}

        future = self.prophet_model.make_future_dataframe(periods=days)
        forecast = self.prophet_model.predict(future)

        forecast_data = forecast.tail(days)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        results = []
        import datetime
        today = datetime.datetime.now()
        
        # Controlled Blending Setup
        transactions = transactions or []
        real_avg = self.get_real_daily_avg(transactions)
        
        if not transactions or real_avg == 0:
            weight = 0.0
        elif len(transactions) < 5:
            weight = 0.1
        else:
            weight = 0.3
            
        adjusted_yhats = []
        for i, (_, row) in enumerate(forecast_data.iterrows()):
            new_date = today + datetime.timedelta(days=i)
            prophet_val = float(row["yhat"])
            
            # Blending calculation
            adjusted = (prophet_val * (1 - weight)) + (real_avg * weight)
            adjusted_yhats.append(adjusted)
            
            results.append({
                "date": new_date.strftime("%Y-%m-%d"),
                "predicted_spend": round(adjusted, 2),
                "lower_bound": round(adjusted * 0.8, 2),
                "upper_bound": round(adjusted * 1.2, 2)
            })

        avg_future_spend = sum(adjusted_yhats) / len(adjusted_yhats) if adjusted_yhats else 0
        
        import pandas as pd
        trend_velocity = pd.Series(adjusted_yhats).diff().mean() if adjusted_yhats else 0

        return {
            "forecast_days": days,
            "avg_future_spend": round(float(avg_future_spend), 2),
            "trend": float(trend_velocity),
            "predictions": results
        }

    def predict_spending_fusion(self, profile_dict: dict, transactions: list = None) -> dict:
        """Phase 4 & 5: Smart Combination and Business Intelligence"""
        # 1. Behavior Score (Stability)
        stability_score = self.evaluate_behavior(profile_dict)
        
        # 2. Temporal Forecast
        forecast_result = self.forecast_spending(days=30, profile_dict=profile_dict, transactions=transactions)
        avg_future_spend_daily = forecast_result.get("avg_future_spend", 0)
        trend = forecast_result.get("trend", 0)
        
        # 3. Fusion Logic Initialization
        income = max(profile_dict.get("monthly_income", 1), 1)
        monthly_forecast = avg_future_spend_daily * 30
        spend_ratio = monthly_forecast / income

        if stability_score < 0.4 and spend_ratio > 0.8:
            status = "High Risk Overspending"
        elif stability_score > 0.7 and spend_ratio < 0.6:
            status = "Financially Stable"
        else:
            status = "Moderate Risk"

        # 4. Insights Generation
        insights = []
        if trend > 0.5:
            insights.append("Spending trend is actively increasing over time.")
        if stability_score < 0.4:
            insights.append("Static behavioral patterns indicate a volatile structural budget.")
        if status == "Financially Stable":
            insights.append("Your temporal spending pace sits safely within your healthy behavioral capacity.")
            
        return {
            "behavior_score": round(stability_score, 2),
            "average_future_spend_daily": avg_future_spend_daily,
            "predicted_monthly_spend": round(monthly_forecast, 2),
            "status": status,
            "trend": trend,
            "insights": insights,
            "predictions": forecast_result["predictions"]
        }


# Singleton instance
spending_forecaster = SpendingForecaster()

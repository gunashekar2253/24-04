from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.profile import FinancialProfile
from app.models.transaction import Transaction
from app.engine.risk_predictor import risk_predictor
from app.engine.spending_forecaster import spending_forecaster
from app.engine.budget_optimizer import budget_optimizer
from app.engine.investment_calculator import investment_calculator

router = APIRouter(prefix="/api/analysis", tags=["Analysis Dashboard"])


@router.get("/dashboard")
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Please complete your financial profile first to generate AI insights.")

    profile_dict = {
        "age": current_user.age,
        "monthly_income": profile.monthly_income,
        "monthly_expenses": profile.monthly_expenses,
        "total_savings": profile.total_savings,
        "loan_amount": profile.loan_amount,
        "monthly_emi": profile.monthly_emi,
        "credit_score": profile.credit_score,
        "credit_card_usage": profile.credit_card_usage
    }

    # 1. Base AI Engines
    risk_assessment = risk_predictor.predict(profile_dict)

    # 2. Transaction Dependent Engines
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.date.desc()).all()
    
    current_month_spending = 0
    recent_anomalies = []
    
    if transactions:
        import datetime
        now = datetime.datetime.now()
        
        from app.engine.anomaly_detector import anomaly_detector

        for t in transactions:
            if t.type == "expense" and t.date.month == now.month and t.date.year == now.year:
                current_month_spending += t.amount
                
            analysis = anomaly_detector.detect(amount=t.amount, balance=profile.total_savings)
            if analysis["is_anomaly"]:
                recent_anomalies.append({
                     "id": t.id,
                     "date": t.date.strftime("%Y-%m-%d"),
                     "amount": t.amount,
                     "description": t.description,
                     "severity": analysis["severity"]
                })
        
        
        # Decision Engine Fusion (Prophet + XGBoost)
        spending_forecast = spending_forecaster.predict_spending_fusion(profile_dict)
    else:
        # Fallback profile-based behavioral model if no transactions exist
        spending_forecast = spending_forecaster.predict_spending_fusion(profile_dict)
        spending_forecast["status"] = "No historical transactions. Behavioral static scaling applied."

    # 3. Dynamic Advisory AI (Cross-Engine Binding)
    budget_optimizations = budget_optimizer.optimize(
        profile_dict,
        risk=risk_assessment,
        forecast=spending_forecast
    )
    
    investments = investment_calculator.calculate(
        profile_dict,
        risk=risk_assessment,
        forecast=spending_forecast
    )

    return {
        "risk_assessment": risk_assessment,
        "budget_optimization": budget_optimizations,
        "investment_capacity": investments,
        "spending_forecast": spending_forecast,
        "transactions_count": len(transactions),
        "recent_anomalies": recent_anomalies
    }

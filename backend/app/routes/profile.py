from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.profile import FinancialProfile
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.engine.risk_predictor import risk_predictor

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.post("", response_model=ProfileResponse)
def create_or_update_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()

    if not profile:
        profile = FinancialProfile(user_id=current_user.id, **profile_in.dict())
        db.add(profile)
    else:
        for key, value in profile_in.dict().items():
            setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    # Get ML risk prediction
    risk_data = risk_predictor.predict({
        "age": current_user.age,
        "monthly_income": profile.monthly_income,
        "monthly_expenses": profile.monthly_expenses,
        "total_savings": profile.total_savings,
        "loan_amount": profile.loan_amount,
        "monthly_emi": profile.monthly_emi,
        "credit_score": profile.credit_score,
        "credit_card_usage": profile.credit_card_usage
    })

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "monthly_income": profile.monthly_income,
        "monthly_expenses": profile.monthly_expenses,
        "total_savings": profile.total_savings,
        "loan_amount": profile.loan_amount,
        "monthly_emi": profile.monthly_emi,
        "credit_score": profile.credit_score,
        "credit_card_usage": profile.credit_card_usage,
        "risk_prediction": risk_data
    }


@router.get("", response_model=ProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get ML risk prediction
    risk_data = risk_predictor.predict({
        "age": current_user.age,
        "monthly_income": profile.monthly_income,
        "monthly_expenses": profile.monthly_expenses,
        "total_savings": profile.total_savings,
        "loan_amount": profile.loan_amount,
        "monthly_emi": profile.monthly_emi,
        "credit_score": profile.credit_score,
        "credit_card_usage": profile.credit_card_usage
    })

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "monthly_income": profile.monthly_income,
        "monthly_expenses": profile.monthly_expenses,
        "total_savings": profile.total_savings,
        "loan_amount": profile.loan_amount,
        "monthly_emi": profile.monthly_emi,
        "credit_score": profile.credit_score,
        "credit_card_usage": profile.credit_card_usage,
        "risk_prediction": risk_data
    }

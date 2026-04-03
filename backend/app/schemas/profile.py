from pydantic import BaseModel
from typing import Optional


class ProfileCreate(BaseModel):
    monthly_income: float
    monthly_expenses: float
    total_savings: float
    loan_amount: float = 0.0
    monthly_emi: float = 0.0
    credit_score: int
    credit_card_usage: float = 0.0


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    monthly_income: float
    monthly_expenses: float
    total_savings: float
    loan_amount: float
    monthly_emi: float
    credit_score: int
    credit_card_usage: float

    class Config:
        from_attributes = True


class ProfileWithPredictions(ProfileResponse):
    """Profile data combined with ML predictions."""
    risk_level: Optional[str] = None
    budget_stability: Optional[float] = None
    savings_ratio: Optional[float] = None
    debt_ratio: Optional[float] = None

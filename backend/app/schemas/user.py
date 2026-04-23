from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    currency: str = "INR"
    age: Optional[int] = None
    monthly_income: float
    monthly_expenses: float
    total_savings: float
    loan_amount: float = 0.0
    monthly_emi: float = 0.0
    credit_score: int
    credit_card_usage: float = 0.0


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    currency: str
    age: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None

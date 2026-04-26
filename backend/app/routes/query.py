from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.profile import FinancialProfile
from app.engine.gemini_chat import gemini_chat

router = APIRouter(prefix="/api/query", tags=["AI Chat"])

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    is_finance: bool
    classification_reason: str


@router.post("/", response_model=ChatResponse)
async def ask_financial_assistant(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    user_profile_dict = None
    if profile:
        user_profile_dict = {
            "age": current_user.age,
            "monthly_income": profile.monthly_income,
            "monthly_expenses": profile.monthly_expenses,
            "total_savings": profile.total_savings,
            "loan_amount": profile.loan_amount,
            "monthly_emi": profile.monthly_emi,
            "credit_score": profile.credit_score,
            "credit_card_usage": profile.credit_card_usage
        }

    # Pass to Gemini engine (It internally uses QueryClassifier to filter)
    result = await gemini_chat.chat(request.query, user_profile=user_profile_dict)

    return {
        "response": result["response"],
        "is_finance": result["is_finance"],
        "classification_reason": result["classification"]["reason"]
    }

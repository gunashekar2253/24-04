from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth import get_current_user
from app.models.user import User
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
):
    # Pass to Gemini engine (It internally uses QueryClassifier to filter)
    result = await gemini_chat.chat(request.query)

    return {
        "response": result["response"],
        "is_finance": result["is_finance"],
        "classification_reason": result["classification"]["reason"]
    }

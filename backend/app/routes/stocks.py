from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import get_current_user
from app.models.user import User
from app.engine.stock_agent import stock_agent

router = APIRouter(prefix="/api/stocks", tags=["Stock Market Agent"])

class StockChatRequest(BaseModel):
    ticker: str
    question: str


@router.get("/analyze/{ticker}")
async def analyze_stock(
    ticker: str,
    current_user: User = Depends(get_current_user),
):
    """Fetches real-time stock data and generates CrewAI analyst insights."""
    result = await stock_agent.analyze_stock(ticker)
    
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result


@router.post("/chat")
async def stock_chat(
    request: StockChatRequest,
    current_user: User = Depends(get_current_user),
):
    """Directly answers questions about a specific stock using CrewAI."""
    answer = await stock_agent.stock_chat(request.ticker, request.question)
    return answer

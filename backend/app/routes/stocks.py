from fastapi import APIRouter, Depends, HTTPException
import yfinance as yf
import logging
from pydantic import BaseModel

from app.models.user import User
from app.auth import get_current_user
from app.engine.stock_agent import stock_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/stocks", tags=["stocks"])

class StockChatRequest(BaseModel):
    ticker: str
    question: str

# Simple in-memory cache
CACHE = {}

def _resolve_ticker_symbol(raw: str) -> str:
    """
    Resolve ticker to correct exchange suffix using naming rules.
    NO API call here — just string logic.
    """
    raw = raw.upper().replace("STOCK", "").strip()

    if "." in raw:
        return raw  # Already has suffix like TCS.NS

    # Known Indian tickers — add .NS directly (no API call needed)
    KNOWN_NSE = {
        "TCS", "RELIANCE", "INFY", "HDFCBANK", "WIPRO",
        "ICICIBANK", "SBIN", "BAJFINANCE", "HINDUNILVR", "ADANIENT"
    }

    if raw in KNOWN_NSE:
        return f"{raw}.NS"

    # Default: assume US ticker
    return raw

def _fetch_stock_data(ticker: str) -> dict:
    """
    ONE single yfinance call to get all data.
    Uses cache to avoid repeat calls.
    """
    raw = ticker.upper().replace("STOCK", "").strip()

    # ✅ Return from cache — no API call at all
    if raw in CACHE:
        logger.info(f"[CACHE HIT] {raw}")
        return CACHE[raw]

    # Resolve the correct ticker symbol (no API call)
    resolved = _resolve_ticker_symbol(raw)
    logger.info(f"[FETCH] Making ONE yfinance call for {resolved}")

    # ✅ ONE single yfinance call
    stock = yf.Ticker(resolved)
    info = stock.info or {}

    # If no price found and no suffix, try .NS once
    has_price = (
        info.get("currentPrice")
        or info.get("regularMarketPrice")
        or info.get("previousClose")
    )

    if not has_price and "." not in resolved:
        logger.info(f"[RETRY] No price found, trying {resolved}.NS")
        resolved = f"{resolved}.NS"
        stock = yf.Ticker(resolved)
        info = stock.info or {}
        has_price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )

    if not has_price:
        raise HTTPException(
            status_code=404,
            detail=f"Stock '{raw}' not found. Try AAPL, TCS, RELIANCE."
        )

    # Get price history in same session
    hist = stock.history(period="1mo")
    price_history = []
    if hist is not None and not hist.empty:
        for date_idx, row in hist.iterrows():
            price_history.append({
                "date": date_idx.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
            })

    current_price = (
        info.get("currentPrice")
        or info.get("regularMarketPrice")
        or info.get("previousClose", 0)
    )

    data = {
        "ticker": resolved,
        "name": info.get("longName") or info.get("shortName", resolved),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "current_price": current_price,
        "market_cap": info.get("marketCap", 0),
        "pe_ratio": info.get("trailingPE") or info.get("forwardPE"),
        "52_week_low": info.get("fiftyTwoWeekLow", 0),
        "52_week_high": info.get("fiftyTwoWeekHigh", 0),
        "price_history": price_history,
        "error": None
    }

    # ✅ Cache it so next call costs zero API hits
    CACHE[raw] = data
    CACHE[resolved] = data  # cache both forms
    return data


@router.get("/analyze/{ticker}")
def analyze_stock(
    ticker: str,
    current_user: User = Depends(get_current_user),
):
    try:
        stock_data = _fetch_stock_data(ticker)
        ai_analysis = stock_agent.analyze_stock(stock_data)
        return {
            "stock_data": stock_data,
            "ai_analysis": ai_analysis,
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"analyze_stock error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/chat")
def stock_chat(
    payload: StockChatRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        stock_data = _fetch_stock_data(payload.ticker)
        answer = stock_agent.stock_chat(payload.ticker, stock_data, payload.question)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"I'm having trouble analyzing {payload.ticker}: {str(e)}"}
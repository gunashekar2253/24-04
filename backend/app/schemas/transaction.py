from pydantic import BaseModel
from typing import Optional
from datetime import date


class TransactionCreate(BaseModel):
    date: date
    category: str
    description: Optional[str] = None
    type: str  # "income" or "expense"
    amount: float


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    date: date
    category: str
    description: Optional[str] = None
    type: str
    amount: float

    class Config:
        from_attributes = True

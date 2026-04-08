from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.engine.anomaly_detector import anomaly_detector

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionResponse)
def add_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = Transaction(
        user_id=current_user.id,
        **transaction_in.dict()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Check for anomaly (assuming passing hardcoded balance based on profile later, but using 0 for isolated detection)
    anomaly_status = anomaly_detector.detect(amount=transaction.amount, balance=transaction.amount)

    return {
        **transaction.__dict__,
        "anomaly_analysis": anomaly_status
    }


@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.date.desc()).all()
    
    results = []
    for t in transactions:
        results.append({
            **t.__dict__,
            "anomaly_analysis": anomaly_detector.detect(amount=t.amount, balance=t.amount)
        })
        
    return results


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    db.delete(transaction)
    db.commit()

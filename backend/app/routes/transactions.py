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
    INCOME_CATEGORIES = {"Salary", "Bonus", "Freelance / Part-time", "Business Income", "Investment Returns", "Other Income"}
    EXPENSE_CATEGORIES = {"Food & Dining", "Housing & Rent", "Transportation", "Utilities", "Entertainment", "Shopping", "Healthcare", "Other Expenses"}

    if transaction_in.type == "income" and transaction_in.category not in INCOME_CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid income category selected.")
    if transaction_in.type == "expense" and transaction_in.category not in EXPENSE_CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid expense category selected.")

    transaction = Transaction(
        user_id=current_user.id,
        **transaction_in.dict()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Check for anomaly using actual profile savings to correctly calculate impact context
    from app.models.profile import FinancialProfile
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    
    if profile:
        if transaction.type == "income":
            profile.total_savings += transaction.amount
        elif transaction.type == "expense":
            profile.total_savings -= transaction.amount
        
        # Enforce baseline
        profile.total_savings = max(profile.total_savings, 0)
        db.commit()

    savings = profile.total_savings if profile else 0
    
    if transaction.type == "expense":
        anomaly_status = anomaly_detector.detect(amount=transaction.amount, balance=savings)
    else:
        anomaly_status = {"is_anomaly": False, "severity": "Normal"}

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
    
    from app.models.profile import FinancialProfile
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    savings = profile.total_savings if profile else 0

    results = []
    for t in transactions:
        if t.type == "expense":
            analysis = anomaly_detector.detect(amount=t.amount, balance=savings)
        else:
            analysis = {"is_anomaly": False, "severity": "Normal"}
            
        results.append({
            **t.__dict__,
            "anomaly_analysis": analysis
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
        
    from app.models.profile import FinancialProfile
    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    
    if profile:
        if transaction.type == "income":
            profile.total_savings -= transaction.amount
        elif transaction.type == "expense":
            profile.total_savings += transaction.amount
            
        profile.total_savings = max(profile.total_savings, 0)
        
    db.delete(transaction)
    db.commit()

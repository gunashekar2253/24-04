from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    monthly_income = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)
    total_savings = Column(Float, nullable=False)
    loan_amount = Column(Float, default=0.0)
    monthly_emi = Column(Float, default=0.0)
    credit_score = Column(Integer, nullable=False)
    credit_card_usage = Column(Float, default=0.0)  # Percentage 0-100

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="profile")

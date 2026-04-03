from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    date = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)  # Shopping, Food, Phone, etc.
    description = Column(String(255), nullable=True)
    type = Column(String(10), nullable=False)  # "income" or "expense"
    amount = Column(Float, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="transactions")

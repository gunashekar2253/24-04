import sys
import os
from datetime import date, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Add backend directory to sys path so we can import app modules directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.profile import FinancialProfile
from app.models.transaction import Transaction
from app.models.goal import Goal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    # Initialize DB tables just in case
    init_db()
    
    db = SessionLocal()
    
    try:
        print("Seeding database...")
        
        # 1. Create Test User
        test_username = "testuser"
        existing_user = db.query(User).filter(User.username == test_username).first()
        if existing_user:
            print("Test user already exists. Cleaning up old data...")
            db.query(Transaction).filter(Transaction.user_id == existing_user.id).delete()
            db.query(Goal).filter(Goal.user_id == existing_user.id).delete()
            db.query(FinancialProfile).filter(FinancialProfile.user_id == existing_user.id).delete()
            db.delete(existing_user)
            db.commit()

        hashed_password = pwd_context.hash("password123")
        user = User(
            username=test_username,
            hashed_password=hashed_password,
            age=30,
            currency="INR"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
        
        # 2. Create Profile
        profile = FinancialProfile(
            user_id=user_id,
            monthly_income=150000.0,
            monthly_expenses=85000.0,
            total_savings=450000.0,
            loan_amount=1200000.0,
            monthly_emi=25000.0,
            credit_score=780,
            credit_card_usage=0.25 # 25%
        )
        db.add(profile)
        
        # 3. Create Transactions (over last 30 days)
        today = date.today()
        transactions = [
            # Income
            Transaction(user_id=user_id, date=today - timedelta(days=3), category="Salary", description="Tech Corp Monthly Salary", type="income", amount=150000.0),
            
            # Expenses
            Transaction(user_id=user_id, date=today - timedelta(days=1), category="Food", description="Starbucks", type="expense", amount=450.0),
            Transaction(user_id=user_id, date=today - timedelta(days=2), category="Food", description="Grocery Store", type="expense", amount=3500.0),
            Transaction(user_id=user_id, date=today - timedelta(days=5), category="Rent", description="Apartment Rent", type="expense", amount=45000.0),
            Transaction(user_id=user_id, date=today - timedelta(days=8), category="Entertainment", description="Netflix Subscription", type="expense", amount=649.0),
            Transaction(user_id=user_id, date=today - timedelta(days=12), category="Utilities", description="Electricity Bill", type="expense", amount=2100.0),
            Transaction(user_id=user_id, date=today - timedelta(days=15), category="Transport", description="Uber Rides", type="expense", amount=1200.0),
            Transaction(user_id=user_id, date=today - timedelta(days=20), category="Investment", description="Mutual Fund SIP", type="expense", amount=15000.0),
            Transaction(user_id=user_id, date=today - timedelta(days=22), category="Other", description="Amazon Shopping", type="expense", amount=5600.0),
            
            # Outlier Anomaly for Isolation Forest to catch
            Transaction(user_id=user_id, date=today - timedelta(days=4), category="Entertainment", description="Luxury Watch Purchase", type="expense", amount=145000.0)
        ]
        db.add_all(transactions)
        
        # 4. Create Goals
        goals = [
            Goal(user_id=user_id, name="Emergency Fund", target_amount=500000.0, current_amount=450000.0, target_date=today + timedelta(days=60)),
            Goal(user_id=user_id, name="Vacation", target_amount=150000.0, current_amount=20000.0, target_date=today + timedelta(days=180)),
            Goal(user_id=user_id, name="Car Downpayment", target_amount=800000.0, current_amount=0.0, target_date=today + timedelta(days=730))
        ]
        db.add_all(goals)
        
        db.commit()
        print(f"Successfully seeded database!")
        print(f"Test Credentials -> Username: {test_username} | Password: password123")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # create scripts directory if it doesn't exist
    seed_database()

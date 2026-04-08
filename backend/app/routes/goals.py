from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import date
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.goal import Goal
from app.models.profile import FinancialProfile
from app.engine.goal_planner import goal_planner

router = APIRouter(prefix="/api/goals", tags=["Goals"])

class GoalCreate(BaseModel):
    name: str
    target_amount: float
    target_date: date
    current_amount: float = 0.0

class GoalResponse(GoalCreate):
    id: int
    user_id: int
    status: str

    class Config:
        orm_mode = True


@router.post("", response_model=GoalResponse)
def create_goal(
    goal_in: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = Goal(
        user_id=current_user.id,
        name=goal_in.name,
        target_amount=goal_in.target_amount,
        target_date=goal_in.target_date,
        current_amount=goal_in.current_amount
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("", response_model=List[GoalResponse])
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Goal).filter(Goal.user_id == current_user.id).all()


@router.post("/{goal_id}/plan")
def get_goal_ai_plan(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    profile = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Financial profile required to generate goal plan.")

    profile_dict = {
        "monthly_income": profile.monthly_income,
        "monthly_expenses": profile.monthly_expenses,
        "monthly_emi": profile.monthly_emi
    }
    
    goal_dict = {
        "name": goal.name,
        "target_amount": goal.target_amount,
        "current_saved": goal.current_amount,
        "priority": "high"  # Arbitrary for the prototype
    }

    plan = goal_planner.plan(goal_dict, profile_dict)
    return plan

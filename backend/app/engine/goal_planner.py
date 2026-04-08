"""
Goal Planner Engine
Provides AI-driven financial goal planning and timeline estimation.
"""
import math


class GoalPlanner:

    def plan(self, goal: dict, profile: dict) -> dict:
        """
        Accepts:
          goal: {name, target_amount, current_saved, priority}
          profile: {monthly_income, monthly_expenses, monthly_emi}
        Returns a timeline and monthly contribution plan.
        """
        target = goal["target_amount"]
        current = goal.get("current_saved", 0)
        remaining = max(0, target - current)

        income = profile["monthly_income"]
        expenses = profile["monthly_expenses"]
        emi = profile.get("monthly_emi", 0)

        # Max monthly contribution = disposable income
        disposable = max(0, income - expenses - emi)

        # Contribution tiers based on priority
        priority = goal.get("priority", "medium").lower()
        if priority == "high":
            contribution_pct = 0.50  # 50% of disposable
        elif priority == "low":
            contribution_pct = 0.15
        else:
            contribution_pct = 0.30

        monthly_contribution = disposable * contribution_pct

        if monthly_contribution <= 0:
            return {
                "goal_name": goal["name"],
                "feasible": False,
                "message": "Your current disposable income does not allow savings toward this goal. "
                           "Consider reducing expenses first.",
                "monthly_contribution": 0,
                "months_needed": None
            }

        months_needed = math.ceil(remaining / monthly_contribution)
        years = months_needed // 12
        leftover_months = months_needed % 12

        timeline_str = ""
        if years > 0:
            timeline_str += f"{years} year{'s' if years > 1 else ''}"
        if leftover_months > 0:
            timeline_str += f" {leftover_months} month{'s' if leftover_months > 1 else ''}"

        # Milestones (25%, 50%, 75%, 100%)
        milestones = []
        for pct in [25, 50, 75, 100]:
            amount_at_pct = target * (pct / 100)
            months_to_pct = math.ceil(max(0, amount_at_pct - current) / monthly_contribution) if monthly_contribution > 0 else 0
            milestones.append({"percentage": pct, "months": months_to_pct})

        return {
            "goal_name": goal["name"],
            "feasible": True,
            "target_amount": round(target, 2),
            "current_saved": round(current, 2),
            "remaining": round(remaining, 2),
            "monthly_contribution": round(monthly_contribution, 2),
            "months_needed": months_needed,
            "timeline": timeline_str.strip(),
            "milestones": milestones
        }


# Singleton instance
goal_planner = GoalPlanner()

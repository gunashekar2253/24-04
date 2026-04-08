"""
Investment Capacity Calculator Engine
Analyzes a user's financial profile to determine safe investment capacity.
"""


class InvestmentCalculator:

    def calculate(self, profile: dict) -> dict:
        """
        Accepts profile dict with: monthly_income, monthly_expenses,
        total_savings, loan_amount, monthly_emi, credit_score
        Returns investment capacity analysis.
        """
        income = profile["monthly_income"]
        expenses = profile["monthly_expenses"]
        emi = profile.get("monthly_emi", 0)
        savings = profile.get("total_savings", 0)
        credit_score = profile.get("credit_score", 600)

        # Disposable income after expenses and EMI
        disposable = max(0, income - expenses - emi)

        # Emergency fund = 6 months of expenses
        emergency_fund_target = expenses * 6
        emergency_fund_status = savings >= emergency_fund_target

        # Safe investment amount = disposable income minus emergency buffer
        emergency_gap = max(0, emergency_fund_target - savings)
        monthly_emergency_contribution = emergency_gap / 12 if emergency_gap > 0 else 0
        safe_monthly_investment = max(0, disposable - monthly_emergency_contribution)

        # Risk tolerance based on credit score and debt ratio
        debt_ratio = (emi) / (income + 1)
        if credit_score >= 750 and debt_ratio < 0.2:
            risk_tolerance = "Aggressive"
            suggested_split = {"equity": 70, "debt_funds": 20, "gold_fd": 10}
        elif credit_score >= 600 and debt_ratio < 0.4:
            risk_tolerance = "Moderate"
            suggested_split = {"equity": 50, "debt_funds": 35, "gold_fd": 15}
        else:
            risk_tolerance = "Conservative"
            suggested_split = {"equity": 20, "debt_funds": 50, "gold_fd": 30}

        recommendations = []
        if not emergency_fund_status:
            recommendations.append(f"Build your emergency fund first. You need ₹{round(emergency_gap, 2)} more.")
        if safe_monthly_investment > 0:
            recommendations.append(f"You can safely invest ₹{round(safe_monthly_investment, 2)} per month.")
        else:
            recommendations.append("Focus on reducing expenses before investing.")

        return {
            "disposable_income": round(disposable, 2),
            "emergency_fund": {
                "target": round(emergency_fund_target, 2),
                "current_savings": round(savings, 2),
                "is_adequate": emergency_fund_status
            },
            "safe_monthly_investment": round(safe_monthly_investment, 2),
            "risk_tolerance": risk_tolerance,
            "suggested_allocation": suggested_split,
            "recommendations": recommendations
        }


# Singleton instance
investment_calculator = InvestmentCalculator()

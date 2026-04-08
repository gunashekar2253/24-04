"""
Budget Optimizer Engine
Provides AI-driven budget recommendations based on the user's financial profile.
"""


class BudgetOptimizer:

    # Ideal allocation percentages (50/30/20 rule adapted)
    IDEAL_ALLOCATION = {
        "needs": 0.50,       # Rent, utilities, groceries, EMI
        "wants": 0.30,       # Entertainment, dining, travel
        "savings": 0.20      # Savings + investments
    }

    def optimize(self, profile: dict) -> dict:
        """
        Accepts profile dict with: monthly_income, monthly_expenses,
        total_savings, loan_amount, monthly_emi, credit_card_usage
        Returns optimized budget plan.
        """
        income = profile["monthly_income"]
        expenses = profile["monthly_expenses"]
        emi = profile.get("monthly_emi", 0)
        savings = profile.get("total_savings", 0)
        cc_usage = profile.get("credit_card_usage", 0)

        # Current ratios
        expense_ratio = expenses / (income + 1)
        savings_rate = max(0, (income - expenses - emi)) / (income + 1)
        debt_burden = (emi + cc_usage * income * 0.2) / (income + 1)

        # Ideal targets
        ideal_needs = income * self.IDEAL_ALLOCATION["needs"]
        ideal_wants = income * self.IDEAL_ALLOCATION["wants"]
        ideal_savings = income * self.IDEAL_ALLOCATION["savings"]

        # Recommendations
        recommendations = []
        if expense_ratio > 0.70:
            recommendations.append("Your expenses exceed 70% of income. Try reducing discretionary spending.")
        if savings_rate < 0.10:
            recommendations.append("Your savings rate is below 10%. Aim for at least 20% of income.")
        if debt_burden > 0.40:
            recommendations.append("Your debt-to-income ratio is high. Consider debt consolidation.")
        if cc_usage > 0.50:
            recommendations.append("Credit card utilization is above 50%. This may impact your credit score.")
        if not recommendations:
            recommendations.append("Your financial health looks great! Keep it up.")

        return {
            "current_snapshot": {
                "expense_ratio": round(expense_ratio * 100, 2),
                "savings_rate": round(savings_rate * 100, 2),
                "debt_burden": round(debt_burden * 100, 2)
            },
            "ideal_budget": {
                "needs": round(ideal_needs, 2),
                "wants": round(ideal_wants, 2),
                "savings_investment": round(ideal_savings, 2)
            },
            "recommendations": recommendations,
            "budget_health": "Good" if expense_ratio < 0.6 and savings_rate > 0.15 else "Needs Improvement"
        }


# Singleton instance
budget_optimizer = BudgetOptimizer()

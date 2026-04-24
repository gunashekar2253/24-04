"""
Budget Optimizer Engine
Provides AI-driven budget recommendations structured dynamically atop baseline ratios.
"""

class BudgetOptimizer:

    def optimize(self, profile: dict, risk: dict = None, forecast: dict = None) -> dict:
        """
        Accepts profile dict, and optionally risk/forecast ML outputs to generate
        a dynamic, scored, and intelligent financial action plan.
        """
        # 1. Foundation Metrics
        income = max(profile.get("monthly_income", 1), 1)
        expenses = profile.get("monthly_expenses", 0)
        emi = profile.get("monthly_emi", 0)
        savings = profile.get("total_savings", 0)
        cc_usage = profile.get("credit_card_usage", 0)

        expense_ratio = expenses / income
        savings_rate = max(0, income - expenses - emi) / income
        debt_ratio = emi / income
        
        # 2. Dynamic Allocations securely tracking over baseline
        allocation = {"needs": 0.50, "wants": 0.30, "savings": 0.20}
        if debt_ratio > 0.4:
            allocation["needs"] = 0.60
            allocation["wants"] = 0.20
            allocation["savings"] = 0.20
        elif savings_rate < 0.1:
            allocation["needs"] = 0.55
            allocation["wants"] = 0.25
            allocation["savings"] = 0.20

        ideal_needs = income * allocation["needs"]
        ideal_wants = income * allocation["wants"]
        ideal_savings = income * allocation["savings"]

        # 3. Gap Analysis
        actual_savings = income - expenses - emi
        savings_gap = ideal_savings - actual_savings
        
        # 4. Severity Scoring (100-bound map)
        score = 100
        score -= min(expense_ratio * 50, 50)
        score -= (0.2 - savings_rate) * 100 if savings_rate < 0.2 else 0
        score -= min(debt_ratio * 40, 40)
        score = max(0, min(100, round(score)))
        
        # 5. SMART Recommendations Generation
        recs = []
        if expense_ratio > 0.60:
            reduction = (expense_ratio - 0.6) * income
            recs.append(f"Reduce expenses by \u20b9{reduction:,.0f}/month to reach your structurally healthy capacity.")
            
        if savings_rate < 0.20 and savings_gap > 0:
            recs.append(f"Increase savings by \u20b9{savings_gap:,.0f}/month to instantly reach your baseline 20% target.")
        elif actual_savings > 0:
            recs.append(f"Excellent savings rate! You are saving \u20b9{actual_savings:,.0f}/month (\u20b9{abs(savings_gap):,.0f} above your baseline).")

        if debt_ratio > 0.40:
            recs.append(f"Your debt ratio ({debt_ratio*100:.1f}%) is dangerously high. Target debt consolidation.")
        cc_usage_pct = cc_usage if cc_usage > 1 else cc_usage * 100
        if cc_usage_pct > 50:
            recs.append(f"Credit limit utilized at {cc_usage_pct:.1f}%! Keep this beneath 50% to shield your Credit Score.")
            
        # 6. Cross-Engine ML Fusion
        if risk and risk.get("risk_score", 0) > 70:
            recs.append("High neural financial risk detected\u2014prioritize emergency savings.")
        
        if forecast:
            monthly_forecast = forecast.get("average_future_spend_daily", 0) * 30
            spend_ratio = monthly_forecast / income
            if spend_ratio > 0.8 or forecast.get("trend", 0) > 0.5:
                recs.append("Your forecast spending pace is mathematically rising\u2014plan cuts now.")
                
        if not recs:
            recs.append("Your financial equilibrium is absolutely perfect. Excellent discipline!")
            
        # Top 5 prioritization to prevent UI pollution
        recommendations = recs[:5]
        
        health_status = "Good" if score > 70 else ("Moderate" if score > 40 else "Needs Improvement")

        return {
            "budget_score": score,
            "health": health_status,
            "gap_analysis": {
                "savings_gap": round(savings_gap, 2)
            },
            "current_snapshot": {
                "expense_ratio": round(expense_ratio * 100, 2),
                "savings_rate": round(savings_rate * 100, 2),
                "debt_ratio": round(debt_ratio * 100, 2)
            },
            "ideal_budget": {
                "needs": round(ideal_needs, 2),
                "wants": round(ideal_wants, 2),
                "savings_investment": round(ideal_savings, 2)
            },
            "recommendations": recommendations,
            "allocation_model": allocation
        }

# Singleton instance
budget_optimizer = BudgetOptimizer()

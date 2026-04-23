"""
Investment Capacity Calculator Engine
Analyzes a user's financial profile into a dynamic, cross-engine AI investment strategist.
"""

class InvestmentCalculator:

    def calculate(self, profile: dict, risk: dict = None, forecast: dict = None) -> dict:
        """
        Accepts profile dict, and optionally risk/forecast ML outputs to generate
        a dynamic, scored, and intelligent investment strategy pipeline.
        """
        # 1. Foundation Metrics
        income = max(profile.get("monthly_income", 1), 1)
        expenses = profile.get("monthly_expenses", 0)
        emi = profile.get("monthly_emi", 0)
        savings = profile.get("total_savings", 0)
        credit_score = profile.get("credit_score", 600)

        # Assuming EMI is built-in to 'expenses' for pure consistency
        disposable = max(0, income - expenses)
        debt_ratio = emi / income

        # 2. Dynamic Emergency Fund Logic
        if debt_ratio > 0.4:
            months = 9
        elif savings < (expenses * 3):
            months = 6
        else:
            months = 4

        emergency_fund_target = expenses * months
        emergency_fund_status = savings >= emergency_fund_target

        # 3. Investment Capacity (Capped logically at 50% max of buffer)
        emergency_gap = max(0, emergency_fund_target - savings)
        monthly_emergency_contribution = min(
            disposable * 0.3, # Don't aggressively suffocate all liquidity strictly for the emergency fund!
            emergency_gap / 12 if emergency_gap > 0 else 0
        )
        safe_monthly_investment = min(
            disposable * 0.5,
            max(0, disposable - monthly_emergency_contribution)
        )

        # 4. Better Risk Profiling (Credit + Debt + Emergency Savings Buffer)
        if credit_score >= 750 and debt_ratio < 0.2 and emergency_fund_status:
            risk_tolerance = "Aggressive"
            suggested_split = {"equity": 70, "debt_funds": 20, "gold_fd": 10}
        elif credit_score >= 650 and debt_ratio < 0.4:
            risk_tolerance = "Moderate"
            suggested_split = {"equity": 50, "debt_funds": 35, "gold_fd": 15}
        else:
            risk_tolerance = "Conservative"
            suggested_split = {"equity": 20, "debt_funds": 50, "gold_fd": 30}
            
        # 4b. Dynamic Allocation Adjustment natively 
        if risk_tolerance == "Aggressive" and not emergency_fund_status:
            suggested_split = {"equity": 50, "debt_funds": 35, "gold_fd": 15} # Throttle comprehensively if emergency buffer isn't healthy yet.

        # 5. Core Scoring Dimension
        score = 100
        if debt_ratio > 0.4:
            score -= 30
        if not emergency_fund_status:
            score -= 30
        if disposable < (income * 0.1):
            score -= 20
        score = max(0, min(100, round(score)))

        # 6. Smart Goal & Strategy Recommendations natively scaled
        recs = []
        if not emergency_fund_status:
            recs.append(f"Prioritize your emergency fund before aggressive investing. You need \u20b9{emergency_gap:,.0f} more.")
            
        if safe_monthly_investment > 0:
            recs.append(f"Safely invest \u20b9{safe_monthly_investment:,.0f}/month via SIP for strategic growth.")
            
            # Simple Time-to-Goal estimation math
            goal = 1000000
            months_to_goal = goal / max(safe_monthly_investment, 1)
            recs.append(f"Following this velocity, you can hit \u20b910L portfolio natively in ~{int(months_to_goal)} months.")
        else:
            recs.append("Extremely tight free liquidity. Focus completely on reducing outgoing expenses before entering market.")

        # 7. Cross-Engine ML Hook Integration
        if risk and risk.get("risk_score", 0) > 70:
            recs.append("High financial ML risk detected\u2014temporarily reduce investment exposure safely.")

        if forecast:
            avg_future_days = forecast.get("average_future_spend_daily", 0)
            if forecast.get("trend", 0) > 0.5 or (avg_future_days * 30) > expenses:
                recs.append("Your temporal spending pace is actively rising\u2014monitor and dynamically throttle investments.")

        return {
            "investment_score": score,
            "disposable_income": round(disposable, 2), # Required by UI Node
            "safe_monthly_investment": round(safe_monthly_investment, 2), # Required by UI Node
            "risk_tolerance": risk_tolerance, # Required by UI Node
            "emergency_fund": {
                "target": round(emergency_fund_target, 2),
                "current_savings": round(savings, 2),
                "is_adequate": emergency_fund_status
            },
            "suggested_allocation": suggested_split,
            "recommendations": recs[:5]
        }


# Singleton instance
investment_calculator = InvestmentCalculator()

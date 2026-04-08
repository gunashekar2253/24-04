"""
Query Classifier Engine
Determines whether a user query is finance-related or not.
Rejects non-financial queries from the AI Assistant.
"""

FINANCE_KEYWORDS = [
    "money", "finance", "bank", "loan", "credit", "debit", "savings", "investment",
    "stock", "share", "mutual fund", "sip", "emi", "interest", "tax", "income",
    "expense", "budget", "salary", "debt", "mortgage", "insurance", "portfolio",
    "dividend", "bond", "forex", "crypto", "bitcoin", "trading", "profit", "loss",
    "revenue", "asset", "liability", "balance", "account", "withdraw", "deposit",
    "nifty", "sensex", "ipo", "etf", "fd", "fixed deposit", "recurring deposit",
    "inflation", "gdp", "rbi", "sebi", "financial", "wealth", "retire", "pension",
    "ppf", "nps", "elss", "gst", "tds", "itr", "capital gain", "net worth",
    "spend", "groceries", "rent", "utility", "bill", "payment", "transaction",
    "anomaly", "forecast", "predict", "risk", "score", "goal", "plan",
]

NON_FINANCE_INDICATORS = [
    "weather", "recipe", "movie", "song", "game", "sport", "joke", "poem",
    "story", "travel destination", "homework", "code", "programming", "write me a",
    "tell me a joke", "who is the president", "what is the capital",
]


class QueryClassifier:

    def is_finance_related(self, query: str) -> dict:
        """
        Check if a query is finance-related.
        Returns classification result with confidence.
        """
        query_lower = query.lower().strip()

        # Check for non-finance indicators first
        for indicator in NON_FINANCE_INDICATORS:
            if indicator in query_lower:
                return {
                    "is_finance": False,
                    "reason": "This query appears to be unrelated to finance.",
                    "rejected_keyword": indicator
                }

        # Check for finance keywords
        matched_keywords = [kw for kw in FINANCE_KEYWORDS if kw in query_lower]

        if matched_keywords:
            return {
                "is_finance": True,
                "reason": "Query is finance-related.",
                "matched_keywords": matched_keywords[:5]
            }

        # Ambiguous: allow it through but flag it
        # Short queries like "help" or "hi" are allowed
        if len(query_lower.split()) <= 3:
            return {
                "is_finance": True,
                "reason": "Short query allowed by default.",
                "matched_keywords": []
            }

        return {
            "is_finance": False,
            "reason": "This query does not appear to be finance-related. Please ask finance-related questions only.",
            "matched_keywords": []
        }


# Singleton instance
query_classifier = QueryClassifier()

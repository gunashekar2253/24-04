"""
Gemini Chat Engine
Provides finance-only AI chat using Google's Gemini API.
Integrates the Query Classifier to reject non-finance queries.
"""
import google.generativeai as genai
from app.config import settings
from app.engine.query_classifier import query_classifier


class GeminiChat:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def chat(self, user_query: str) -> dict:
        """
        Process a user query through the finance filter and respond using Gemini.
        """
        # Step 1: Classify the query
        classification = query_classifier.is_finance_related(user_query)

        if not classification["is_finance"]:
            return {
                "response": "I can only assist with finance-related questions. "
                            "Please ask about budgeting, investments, loans, savings, or other financial topics.",
                "is_finance": False,
                "classification": classification
            }

        # Step 2: Send to Gemini with a finance-focused system prompt
        system_prompt = (
            "You are a professional financial advisor AI assistant. "
            "You ONLY answer finance-related questions including budgeting, saving, investing, "
            "loans, credit scores, taxes, insurance, and financial planning. "
            "If the user asks anything unrelated to finance, politely decline and redirect. "
            "Provide clear, actionable, and concise financial advice. "
            "Use Indian Rupees (₹) as the default currency unless specified otherwise."
        )

        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser Question: {user_query}"
            )
            answer = response.text
        except Exception as e:
            if "exhausted" in str(e).lower() or "429" in str(e):
                answer = "I'm currently unable to access my deep-learning systems because the Google Gemini API key has exceeded its quota limit! We can resume our conversation once the tokens refresh. Ask me again later."
            else:
                answer = f"Sorry, I encountered an error while processing your request: {str(e)}"

        return {
            "response": answer,
            "is_finance": True,
            "classification": classification
        }


# Singleton instance
gemini_chat = GeminiChat()

import google.generativeai as genai
from app.config import settings
from app.engine.query_classifier import query_classifier

class GeminiChat:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    async def chat(self, query: str, user_profile: dict = None) -> dict:
        classification = query_classifier.is_finance_related(query)
        
        if not classification["is_finance"]:
            return {
                "response": "I am a financial AI assistant. " + classification.get("reason", "I cannot help with that query."),
                "is_finance": False,
                "classification": classification
            }

        if not self.model:
            return {
                "response": "Gemini API key is not configured in the environment.",
                "is_finance": True,
                "classification": classification
            }

        try:
            context = ""
            if user_profile:
                context = (
                    f"\nUser Profile context:\n"
                    f"- Age: {user_profile.get('age', 'N/A')}\n"
                    f"- Monthly Income: ₹{user_profile.get('monthly_income', 0):,}\n"
                    f"- Monthly Expenses: ₹{user_profile.get('monthly_expenses', 0):,}\n"
                    f"- Total Savings: ₹{user_profile.get('total_savings', 0):,}\n"
                    f"- Loan Amount: ₹{user_profile.get('loan_amount', 0):,}\n"
                    f"- Monthly EMI: ₹{user_profile.get('monthly_emi', 0):,}\n"
                    f"- Credit Score: {user_profile.get('credit_score', 'N/A')}\n"
                    f"- Credit Card Usage: {user_profile.get('credit_card_usage', 'N/A')}%\n"
                    "Use this profile context to provide personalized financial analysis and advice. Do not mention that you received this system data, simply use it effectively.\n"
                )

            prompt = f"""You are a helpful and knowledgeable financial AI assistant from India. 
Always use Indian Rupees (₹) for all currency values. Avoid using dollars.

You are a strictly conservative financial advisor. 
The user prefers SAFE investment options only. Do NOT suggest any risky investments such as:
- Stocks
- Equity mutual funds
- Cryptocurrency
- High-risk trading

Focus only on low-risk and stable financial options like:
- Fixed Deposits (FD)
- Public Provident Fund (PPF)
- Recurring Deposits (RD)
- Savings accounts
- Emergency fund planning

Give clear, practical, and realistic advice based on the user's income, expenses, and savings.
Avoid any suggestion where there is a possibility of loss.
Explain recommendations in simple terms and prioritize capital safety over high returns.

If the user asks for stock information, stock data, or analysis about a specific company, reply exactly with: REDIRECT_TO_STOCK: [TICKER_SYMBOL]. For example, REDIRECT_TO_STOCK: AAPL or REDIRECT_TO_STOCK: TCS.NS. Do not include any other text or disclaimers. {context}
Otherwise, answer the user normally. The user asks: {query}"""
            # Some environments might not support async generating, fallback gracefully if so
            result = await self.model.generate_content_async(prompt)
            return {
                "response": result.text,
                "is_finance": True,
                "classification": classification
            }
        except AttributeError:
            result = self.model.generate_content(prompt)
            return {
                "response": result.text,
                "is_finance": True,
                "classification": classification
            }
        except Exception as e:
            return {
                "response": f"An error occurred while generating the response: {str(e)}",
                "is_finance": True,
                "classification": classification
            }

gemini_chat = GeminiChat()

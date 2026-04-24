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

    async def chat(self, query: str) -> dict:
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
            prompt = f"""You are a helpful and knowledgeable financial AI assistant. 
If the user asks for stock information, stock data, or analysis about a specific company, reply exactly with: REDIRECT_TO_STOCK: [TICKER_SYMBOL]. For example, REDIRECT_TO_STOCK: AAPL or REDIRECT_TO_STOCK: TCS.NS. Do not include any other text or disclaimers. 
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

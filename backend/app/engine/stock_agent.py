"""
Stock Agent Engine
Uses CrewAI + yfinance to analyze stocks and provide AI-driven stock insights.
"""
import yfinance as yf
import requests
import time
from cachetools import TTLCache
import threading

class StockAgent:
    
    def analyze_stock(self, stock_data: dict) -> str:
        """Use Gemini LLM to generate an AI analysis based purely on the provided structured dataset."""
        try:
            import requests
            from app.config import settings
            
            prompt = f"""You are an expert equity research analyst.
            Analyze this stock data and provide a brief investment summary:
            Stock: {stock_data.get('name')} ({stock_data.get('ticker')})
            Current Price: {stock_data.get('current_price')}
            Market Cap: {stock_data.get('market_cap')}
            P/E Ratio: {stock_data.get('pe_ratio')}
            52-Week High: {stock_data.get('52_week_high')}
            52-Week Low: {stock_data.get('52_week_low')}
            Sector: {stock_data.get('sector')}

            Provide:
            1. Brief summary (2-3 lines)
            2. Key strengths and risks
            3. Buy/Hold/Sell recommendation with reasoning
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}")
                
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"

    def stock_chat(self, ticker: str, stock_data: dict, question: str) -> str:
        """Answer a follow-up question based on the provided data payload."""
        try:
            import requests
            from app.config import settings

            prompt = f"""You are a friendly stock market expert.
            Answer this user's question about {ticker} ({stock_data.get('name', ticker)}):
            Current Price: {stock_data.get('current_price', 'N/A')}
            Sector: {stock_data.get('sector', 'N/A')}

            User Question: {question}

            Provide a clear, concise answer.
            """
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.5}
            }
            
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}")
                
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Could not process your question: {str(e)}"

# Singleton instance
stock_agent = StockAgent()


import os
from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()

class AIAnalysisService:
    def __init__(self):
        self.client = None
        if settings.openai_api_key:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_stock_analysis(self, company_name: str, symbol: str) -> str:
        """
        Generates stock analysis content using OpenAI based on the prompt template.
        """
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not set")

        # Read prompt template
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "stock_analysis.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            # Fallback if file not found locally (in container vs local)
            # Try relative to route
            prompt_path = "app/prompts/stock_analysis.txt"
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()

        # Fill template
        prompt = template.replace("{{company_name}}", company_name).replace("{{symbol}}", symbol)

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Use a capable model
                messages=[
                    {"role": "system", "content": "You are a professional Thai stock analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating analysis for {symbol}: {e}")
            return None

_service = None

def get_ai_service() -> AIAnalysisService:
    global _service
    if not _service:
        _service = AIAnalysisService()
    return _service

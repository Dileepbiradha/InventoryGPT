import google.generativeai as genai
from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

def ask_gemini(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"""
LLM service temporarily unavailable.

Gemini Error:
{str(e)}
"""
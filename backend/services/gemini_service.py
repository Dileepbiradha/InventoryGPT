import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


def ask_gemini(question):

    response = model.generate_content(
        question
    )

    return response.text
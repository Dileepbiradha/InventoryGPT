import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)


def ask_gemini(question):

    model = genai.GenerativeModel(
        "gemini-2.0-flash"
    )

    response = model.generate_content(
        question
    )

    return response.text
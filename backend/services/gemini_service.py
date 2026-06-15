import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def ask_gemini(question):

    print("QUESTION:", question)

    response = model.generate_content(question)

    print("RESPONSE:", response.text)

    return response.text
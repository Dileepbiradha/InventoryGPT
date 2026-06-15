import google.generativeai as genai

from config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)


def ask_gemini(question):

    available_models = []

    for model in genai.list_models():

        available_models.append({
            "name": model.name,
            "methods": model.supported_generation_methods
        })

    return str(available_models)
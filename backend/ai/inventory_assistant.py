from google import genai
from config import Config


class InventoryAssistant:

    @staticmethod
    def ask(prompt):

        try:

            client = genai.Client(
                api_key=Config.GEMINI_API_KEY
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print("GEMINI ERROR:", str(e))

            raise e
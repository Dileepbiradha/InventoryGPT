import os

import google.generativeai as genai

from dotenv import load_dotenv

from ai.rag_service import RAGService

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class InventoryAssistant:

    @staticmethod
    def answer(question):

        inventory_context = (
            RAGService.build_inventory_context()
        )

        prompt = f"""
You are an Inventory Management Assistant.

Inventory Data:

{inventory_context}

User Question:
{question}

Answer naturally and professionally.
"""

        try:

            # Temporary mock AI response
            if "laptop" in question.lower():

                return (
                    "There are currently 110 laptops in stock. "
                    "The product belongs to the Electronics category "
                    "and is supplied by Dell."
                )

            return inventory_context

        except Exception as e:

            return f"Gemini Error: {str(e)}"
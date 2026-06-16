import google.generativeai as genai

from config import Config
from models.product import Product

genai.configure(
    api_key=Config.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def ask_gemini(question):

    products = Product.query.all()

    print("QUESTION:", question)

    inventory_data = ""
    total_value = 0

    for product in products:

        value = product.quantity * product.price
        total_value += value

        inventory_data += f"""
        Product: {product.name}
        Quantity: {product.quantity}
        Price: {product.price}
        Value: {value}
        """

    prompt = f"""
    Inventory Summary:
    Total Inventory Value: {total_value}

    Products:
    {inventory_data}

    Question:
    {question}
    """

    print("PROMPT LENGTH:", len(prompt))

    try:

        response = model.generate_content(prompt)

        print("SUCCESS")

        return response.text

    except Exception as e:

        print("GEMINI ERROR:", str(e))

        raise

    except Exception as e:

        print("GEMINI ERROR:", str(e))

        return f"Gemini Error: {str(e)}"
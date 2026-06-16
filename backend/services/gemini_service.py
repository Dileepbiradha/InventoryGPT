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
    You are an Inventory Management AI.

    Inventory Summary:

    Total Inventory Value: {total_value}

    Products:

    {inventory_data}

    User Question:

    {question}

    Answer using the inventory data above.
    """

    print("========== PROMPT ==========")
    print(prompt)
    print("============================")

    response = model.generate_content(prompt)

    return response.text
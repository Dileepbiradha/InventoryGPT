from flask import Blueprint
from flask import jsonify
from flask import request

from models.product import Product
from ai.inventory_assistant import InventoryAssistant

ai_bp = Blueprint(
    "ai",
    __name__
)


@ai_bp.route("/ask", methods=["POST"])
def ask_ai():

    try:

        data = request.get_json()

        question = data.get("question")

        products = Product.query.all()

        inventory_context = ""

        for p in products:
            inventory_context += f"""
            Product: {p.name}
            SKU: {p.sku}
            Category: {p.category}
            Quantity: {p.quantity}
            Price: {p.price}
            Supplier: {p.supplier}
            """

        prompt = f"""
        You are InventoryGPT.

        Inventory Data:

        {inventory_context}

        User Question:

        {question}

        Rules:
        - Answer only from inventory data.
        - Keep answers short.
        """

        answer = InventoryAssistant.ask(prompt)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("AI ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500
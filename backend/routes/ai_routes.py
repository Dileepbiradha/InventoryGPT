from flask import Blueprint
from flask import jsonify
from flask import request

from ai.inventory_assistant import InventoryAssistant

ai_bp = Blueprint(
    "ai",
    __name__
)


@ai_bp.route(
    "/ask",
    methods=["POST"]
)
def ask_ai():

    data = request.get_json()

    answer = InventoryAssistant.answer(
        data["question"]
    )

    return jsonify({
        "answer": answer
    })
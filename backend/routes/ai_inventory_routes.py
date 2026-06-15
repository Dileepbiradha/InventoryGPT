from flask import Blueprint
from flask import request
from flask import jsonify

from services.gemini_service import ask_gemini

ai_inventory_bp = Blueprint(
    "ai_inventory",
    __name__
)


@ai_inventory_bp.route(
    "/",
    methods=["GET", "POST"]
)
def ask_inventory_ai():

    if request.method == "GET":
        return jsonify({
            "status": "AI route working"
        })

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    question = data.get(
        "question",
        ""
    )

    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400

    try:

        answer = ask_gemini(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
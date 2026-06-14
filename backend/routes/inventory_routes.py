from flask import Blueprint
from flask import jsonify
from flask import request

from models.transaction import Transaction
from services.inventory_service import InventoryService

inventory_bp = Blueprint(
    "inventory",
    __name__
)


# =========================
# STOCK IN
# =========================
@inventory_bp.route(
    "/stock-in",
    methods=["POST"]
)
def stock_in():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id:
        return jsonify({
            "error": "product_id is required"
        }), 400

    if not quantity:
        return jsonify({
            "error": "quantity is required"
        }), 400

    try:

        product = InventoryService.stock_in(
            product_id,
            quantity
        )

        return jsonify(
            product.to_dict()
        ), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# =========================
# STOCK OUT
# =========================
@inventory_bp.route(
    "/stock-out",
    methods=["POST"]
)
def stock_out():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id:
        return jsonify({
            "error": "product_id is required"
        }), 400

    if not quantity:
        return jsonify({
            "error": "quantity is required"
        }), 400

    try:

        product = InventoryService.stock_out(
            product_id,
            quantity
        )

        return jsonify(
            product.to_dict()
        ), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# =========================
# TRANSACTION HISTORY
# =========================
@inventory_bp.route(
    "/history",
    methods=["GET"]
)
def transaction_history():

    transactions = (
        Transaction.query
        .order_by(
            Transaction.created_at.desc()
        )
        .all()
    )

    return jsonify([
        transaction.to_dict()
        for transaction in transactions
    ])
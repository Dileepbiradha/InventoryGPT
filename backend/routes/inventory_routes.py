from flask import Blueprint
from flask import jsonify
from flask import request

from models.transaction import Transaction

from services.inventory_service import InventoryService

inventory_bp = Blueprint(
    "inventory",
    __name__
)


# STOCK IN
@inventory_bp.route(
    "/stock-in",
    methods=["POST"]
)
def stock_in():

    data = request.get_json()

    product = InventoryService.stock_in(
        data["product_id"],
        data["quantity"]
    )

    return jsonify(
        product.to_dict()
    )


# STOCK OUT
@inventory_bp.route(
    "/stock-out",
    methods=["POST"]
)
def stock_out():

    data = request.get_json()

    product = InventoryService.stock_out(
        data["product_id"],
        data["quantity"]
    )

    return jsonify(
        product.to_dict()
    )

@inventory_bp.route(
    "/history",
    methods=["GET"]
)
def transaction_history():

    transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).all()

    return jsonify([
        transaction.to_dict()
        for transaction in transactions
    ])
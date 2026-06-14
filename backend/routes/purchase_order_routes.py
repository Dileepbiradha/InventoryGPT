from flask import Blueprint, jsonify

from models.purchase_order import PurchaseOrder

from flask import request

from services.purchase_order_service import (
    PurchaseOrderService
)

purchase_order_bp = Blueprint(
    "purchase_orders",
    __name__
)

@purchase_order_bp.route(
    "/<int:order_id>/approve",
    methods=["POST"]
)
def approve_purchase_order(order_id):
    try:
        order = PurchaseOrderService.approve_order(order_id)
        return jsonify(order.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@purchase_order_bp.route("/", methods=["GET"])
def get_purchase_orders():

    orders = PurchaseOrder.query\
        .order_by(
            PurchaseOrder.created_at.desc()
        )\
        .all()

    return jsonify([
        order.to_dict()
        for order in orders
    ])
from flask import Blueprint, jsonify, request

from extensions import db
from models.purchase_order import PurchaseOrder
from services.purchase_order_service import PurchaseOrderService

purchase_order_bp = Blueprint(
    "purchase_orders",
    __name__
)


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


@purchase_order_bp.route("/", methods=["POST"])
def create_purchase_order():

    try:
        data = request.get_json() or {}

        product_id = data.get("product_id")
        quantity = data.get("quantity")
        supplier = data.get("supplier", "Default Supplier")

        if not product_id:
            return jsonify({
                "error": "product_id is required"
            }), 400

        if not quantity or int(quantity) <= 0:
            return jsonify({
                "error": "quantity must be greater than 0"
            }), 400

        order = PurchaseOrder(
            product_id=int(product_id),
            quantity=int(quantity),
            supplier=supplier,
            status="Pending"
        )

        db.session.add(order)
        db.session.commit()

        return jsonify(
            order.to_dict()
        ), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400


@purchase_order_bp.route(
    "/<int:order_id>/approve",
    methods=["POST"]
)
def approve_purchase_order(order_id):

    try:
        order = PurchaseOrderService.approve_order(
            order_id
        )

        return jsonify(
            order.to_dict()
        ), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400
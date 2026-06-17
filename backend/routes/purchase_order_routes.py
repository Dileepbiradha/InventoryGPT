from flask import Blueprint
from flask import jsonify
from flask import request

from extensions import db

from models.purchase_order import PurchaseOrder

from services.purchase_order_service import (
    PurchaseOrderService
)

purchase_order_bp = Blueprint(
    "purchase_orders",
    __name__
)


# GET ALL PURCHASE ORDERS

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


# CREATE PURCHASE ORDER

@purchase_order_bp.route("/", methods=["POST"])
def create_purchase_order():

    try:

        data = request.get_json()

        order = PurchaseOrder(
            product_id=data["product_id"],
            quantity=data["quantity"],
            supplier=data["supplier"],
            status="Pending"
        )

        db.session.add(order)
        db.session.commit()

        return jsonify(
            order.to_dict()
        ), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# APPROVE PURCHASE ORDER

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
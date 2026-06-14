from flask import Blueprint
from flask import jsonify
from flask import request

from extensions import db

from models.sales_order import SalesOrder
from models.product import Product
from models.transaction import Transaction

sales_order_bp = Blueprint(
    "sales_orders",
    __name__
)


@sales_order_bp.route(
    "/",
    methods=["GET"]
)
def get_orders():

    orders = SalesOrder.query.all()

    return jsonify([
        order.to_dict()
        for order in orders
    ])


@sales_order_bp.route(
    "/",
    methods=["POST"]
)
def create_order():

    data = request.get_json()

    product = Product.query.get(
        data["product_id"]
    )

    total_amount = (
    product.price *
    data["quantity"]
    )

    order = SalesOrder(
    customer_id=data["customer_id"],
    product_id=data["product_id"],
    quantity=data["quantity"],
    total_amount=total_amount
    )

    db.session.add(order)
    db.session.commit()

    return jsonify(
        order.to_dict()
    )


@sales_order_bp.route(
    "/<int:order_id>/approve",
    methods=["POST"]
)
def approve_order(order_id):

    order = SalesOrder.query.get_or_404(
        order_id
    )

    if order.status == "Approved":
        return jsonify({
            "error":
            "Already approved"
        }), 400

    product = Product.query.get(
        order.product_id
    )

    if not product:
        return jsonify({
            "error":
            "Product not found"
        }), 404

    if product.quantity < order.quantity:
        return jsonify({
            "error":
            "Insufficient stock"
        }), 400

    product.quantity -= order.quantity

    transaction = Transaction(
        product_id=product.id,
        transaction_type="OUT",
        quantity=order.quantity
    )

    db.session.add(transaction)

    order.status = "Approved"

    db.session.commit()

    return jsonify({
        "message":
        "Sales order approved"
    })
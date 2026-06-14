from flask import Blueprint
from flask import jsonify

from models.product import Product
from models.transaction import Transaction
from models.sales_order import SalesOrder

analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("", methods=["GET"])
def analytics():

    approved_orders = SalesOrder.query.filter_by(
    status="Approved"
    ).all()

    total_revenue = 0

    for order in approved_orders:

        product = Product.query.get(
        order.product_id
    )

    if product:
        total_revenue += (
            product.price *
            order.quantity
        )

    products = Product.query.all()
    transactions = Transaction.query.all()

    inventory_value = sum(
        p.price * p.quantity
        for p in products
    )

    low_stock_count = len([
        p for p in products
        if p.quantity < 20
    ])

    top_stock_product = None

    if products:
        top_stock_product = max(
            products,
            key=lambda p: p.quantity
        ).to_dict()

    # TOP SELLING PRODUCTS

    top_selling = []

    approved_orders = (
        SalesOrder.query.filter_by(
            status="Approved"
        ).all()
    )

    sales_map = {}

    for order in approved_orders:

        product = Product.query.get(
            order.product_id
        )

        if product:

            sales_map[product.name] = (
                sales_map.get(
                    product.name,
                    0
                )
                + order.quantity
            )

    for name, qty in sales_map.items():

        top_selling.append({
            "name": name,
            "quantity": qty
        })

    return jsonify({
        "inventory_value":
            inventory_value,

        "total_products":
            len(products),

        "transaction_count":
            len(transactions),

        "low_stock_count":
            low_stock_count,

        "top_stock_product":
            top_stock_product,

        "top_selling":
            top_selling,
        
        "total_revenue": 
            total_revenue
    })
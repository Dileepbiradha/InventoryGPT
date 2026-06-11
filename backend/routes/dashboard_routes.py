from flask import Blueprint
from flask import jsonify

from models.product import Product

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/", methods=["GET"])
def dashboard_summary():

    products = Product.query.all()

    total_products = len(products)

    inventory_value = sum(
        product.price * product.quantity
        for product in products
    )

    low_stock = len([
        product
        for product in products
        if product.quantity < 10
    ])

    return jsonify({
        "total_products": total_products,
        "inventory_value": inventory_value,
        "low_stock": low_stock
    })
from flask import Blueprint
from flask import jsonify

from models.product import Product

low_stock_bp = Blueprint(
    "low_stock",
    __name__
)

@low_stock_bp.route(
    "",
    methods=["GET"]
)
def low_stock():

    products = Product.query.all()

    low_stock_products = []

    for product in products:

        minimum_stock = (
            product.minimum_stock or 20
        )

        if product.quantity < minimum_stock:

            low_stock_products.append(
                product.to_dict()
            )

    return jsonify(
        low_stock_products
    )
from flask import Blueprint
from flask import jsonify

from extensions import db
from models.purchase_order import PurchaseOrder
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

            existing_order = PurchaseOrder.query.filter_by(
            product_id=product.id,
            status="Pending"
        ).first()

        if not existing_order:

            purchase_order = PurchaseOrder(
                product_id=product.id,
                quantity=50,
                supplier=product.supplier,
                status="Pending"
            )

            db.session.add(
                purchase_order
            )

        low_stock_products.append(
            product.to_dict()
        )

    return jsonify(
        low_stock_products
    )
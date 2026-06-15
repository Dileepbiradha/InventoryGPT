from flask import Blueprint
from flask import jsonify

from models.product import Product
from models.transaction import Transaction

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/", methods=["GET"])
def dashboard():

    products = Product.query.all()

    total_products = len(products)

    inventory_value = sum(
        p.price * p.quantity
        for p in products
    )

    low_stock = [
        p.to_dict()
        for p in products
        if p.quantity < 20
    ]

    recent_transactions = (
        Transaction.query
        .order_by(
            Transaction.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return jsonify({
        "total_products": total_products,
        "inventory_value": inventory_value,

        "low_stock": low_stock,

        "products": [
            p.to_dict()
            for p in products
        ],

        "recent_transactions": [
            t.to_dict()
            for t in recent_transactions
        ]
    })
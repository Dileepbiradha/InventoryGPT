from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required

from services.product_service import ProductService
from models.product import Product
from models.transaction import Transaction

from utils.validators import validate_product
from extensions import db

from decorators.role_required import admin_required


product_bp = Blueprint(
    "products",
    __name__
)


# ==========================================
# GET ALL PRODUCTS
# ==========================================
@product_bp.route(
    "/",
    methods=["GET"]
)
def get_products():

    products = ProductService.get_all()

    return jsonify([
        product.to_dict()
        for product in products
    ])


# ==========================================
# GET PRODUCT BY ID
# ==========================================
@product_bp.route(
    "/<int:id>",
    methods=["GET"]
)
@jwt_required()
def get_product(id):

    product = ProductService.get_by_id(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(
        product.to_dict()
    )


# ==========================================
# CREATE PRODUCT
# ==========================================
@product_bp.route("/", methods=["POST"])
def create_product():

    data = request.get_json()

    product = Product(
        name=data["name"],
        sku=data["sku"],
        quantity=data["quantity"],
        price=data["price"],
        supplier=data["supplier"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created"
    }), 201


# ==========================================
# UPDATE PRODUCT
# ==========================================
@product_bp.route(
    "/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def update_product(id):

    product = ProductService.get_by_id(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    data = request.get_json()

    updated_product = ProductService.update(
        product,
        data
    )

    return jsonify(
        updated_product.to_dict()
    )


# ==========================================
# DELETE PRODUCT
# ==========================================
@product_bp.route(
    "/<int:product_id>",
    methods=["DELETE"]
)
@jwt_required()
@admin_required
def delete_product(product_id):

    product = ProductService.get_by_id(
        product_id
    )

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    ProductService.delete(product)

    return jsonify({
        "message": "Product deleted successfully"
    })


# ==========================================
# SEARCH PRODUCTS
# ==========================================
@product_bp.route(
    "/search",
    methods=["GET"]
)
def search_products():

    q = request.args.get(
        "q",
        ""
    )

    products = Product.query.filter(
        Product.name.ilike(
            f"%{q}%"
        )
    ).all()

    return jsonify([
        product.to_dict()
        for product in products
    ])


# ==========================================
# STOCK IN
# ==========================================
@product_bp.route(
    "/<int:id>/stock-in",
    methods=["POST"]
)
def stock_in(id):

    product = Product.query.get_or_404(id)

    data = request.get_json()

    qty = int(data["quantity"])

    product.quantity += qty

    transaction = Transaction(
        product_id=product.id,
        transaction_type="IN",
        quantity=qty
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Stock added successfully"
    })


# ==========================================
# STOCK OUT
# ==========================================
@product_bp.route(
    "/<int:id>/stock-out",
    methods=["POST"]
)
def stock_out(id):

    product = Product.query.get_or_404(id)

    data = request.get_json()

    qty = int(data["quantity"])

    if product.quantity < qty:
        return jsonify({
            "error": "Insufficient stock"
        }), 400

    product.quantity -= qty

    transaction = Transaction(
        product_id=product.id,
        transaction_type="OUT",
        quantity=qty
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Stock removed successfully"
    })
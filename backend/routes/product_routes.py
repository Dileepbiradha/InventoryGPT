from flask import Blueprint, jsonify, request

from services.product_service import ProductService
from models.product import Product

from utils.validators import validate_product

product_bp = Blueprint(
    "products",
    __name__
)


# GET ALL PRODUCTS
@product_bp.route("/", methods=["GET"])
def get_products():

    products = ProductService.get_all()

    return jsonify([
        product.to_dict()
        for product in products
    ])


# GET PRODUCT BY ID
@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):

    product = ProductService.get_by_id(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict())


# CREATE PRODUCT
@product_bp.route("/", methods=["POST"])
def create_product():

    data = request.get_json()

    errors = validate_product(data)

    if errors:
        return jsonify({
            "errors": errors
        }), 400

    product = ProductService.create(data)

    return jsonify(
        product.to_dict()
    ), 201

# UPDATE PRODUCT
@product_bp.route("/<int:id>", methods=["PUT"])
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


# DELETE PRODUCT
@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):

    product = ProductService.get_by_id(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    ProductService.delete(product)

    return jsonify({
        "message": "Product deleted successfully"
    })


# SEARCH PRODUCTS
@product_bp.route("/search", methods=["GET"])
def search_products():

    q = request.args.get("q", "")

    products = Product.query.filter(
        Product.name.ilike(f"%{q}%")
    ).all()

    return jsonify([
        product.to_dict()
        for product in products
    ])
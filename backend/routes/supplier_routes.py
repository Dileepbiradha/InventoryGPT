from flask import Blueprint
from flask import request
from flask import jsonify

from models.supplier import Supplier
from extensions import db

supplier_bp = Blueprint(
    "suppliers",
    __name__
)

@supplier_bp.route(
    "/",
    methods=["GET"]
)
def get_suppliers():

    suppliers = Supplier.query.all()

    return jsonify([
        supplier.to_dict()
        for supplier in suppliers
    ])

@supplier_bp.route("/", methods=["POST"])
def create_supplier():

    data = request.get_json()

    supplier = Supplier(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        address=data["address"]
    )

    db.session.add(supplier)
    db.session.commit()

    return jsonify(
        supplier.to_dict()
    ), 201

@supplier_bp.route("/<int:id>", methods=["PUT"])
def update_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    data = request.get_json()

    supplier.name = data["name"]
    supplier.email = data["email"]
    supplier.phone = data["phone"]
    supplier.address = data["address"]

    db.session.commit()

    return jsonify(
        supplier.to_dict()
    )

@supplier_bp.route("/<int:id>", methods=["DELETE"])
def delete_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    db.session.delete(supplier)
    db.session.commit()

    return jsonify({
        "message": "Supplier deleted"
    })
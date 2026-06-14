from flask import Blueprint
from flask import jsonify
from flask import request

from extensions import db
from models.customer import Customer

customer_bp = Blueprint(
    "customers",
    __name__
)


@customer_bp.route(
    "/",
    methods=["GET"]
)
def get_customers():

    customers = Customer.query.all()

    return jsonify([
        customer.to_dict()
        for customer in customers
    ])


@customer_bp.route(
    "/",
    methods=["POST"]
)
def create_customer():

    data = request.get_json()

    customer = Customer(
        name=data["name"],
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address")
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify(
        customer.to_dict()
    ), 201


@customer_bp.route(
    "/<int:customer_id>",
    methods=["PUT"]
)
def update_customer(customer_id):

    customer = Customer.query.get_or_404(
        customer_id
    )

    data = request.get_json()

    customer.name = data["name"]
    customer.email = data.get("email")
    customer.phone = data.get("phone")
    customer.address = data.get("address")

    db.session.commit()

    return jsonify(
        customer.to_dict()
    )


@customer_bp.route(
    "/<int:customer_id>",
    methods=["DELETE"]
)
def delete_customer(customer_id):

    customer = Customer.query.get_or_404(
        customer_id
    )

    db.session.delete(customer)
    db.session.commit()

    return jsonify({
        "message":
        "Customer deleted successfully"
    })
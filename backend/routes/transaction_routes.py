from flask import Blueprint
from flask import jsonify

from models.transaction import Transaction

transaction_bp = Blueprint(
    "transactions",
    __name__
)


@transaction_bp.route("/", methods=["GET"])
def get_transactions():

    transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).all()

    return jsonify([
        t.to_dict()
        for t in transactions
    ])


@transaction_bp.route(
    "/history",
    methods=["GET"]
)
def get_history():

    transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).all()

    return jsonify([
        t.to_dict()
        for t in transactions
    ])
from flask import Blueprint
from flask import request
from flask import jsonify

from services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/test")
def test():
    return {"message": "auth blueprint loaded"}


@auth_bp.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        user = AuthService.register(data)

        return jsonify(user), 201

    except ValueError as e:

        return jsonify({
            "message": str(e)
        }), 400


@auth_bp.route("/login", methods=["POST"])

def login():

    try:

        data = request.get_json()

        result = AuthService.login(data)

        return jsonify(result)

    except ValueError as e:

        return jsonify({
            "message": str(e)
        }), 401

    except Exception as e:

        return jsonify({
            "message": str(e)
        }), 500
from flask import Blueprint
from flask import request
from flask import jsonify

from services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()

    user = AuthService.register(
        data
    )

    return jsonify(user), 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    result = AuthService.login(
        data
    )

    return jsonify(result)
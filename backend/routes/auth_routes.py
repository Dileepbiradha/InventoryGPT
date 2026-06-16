from backend import app
from flask import Blueprint
from flask import request
from flask import jsonify

from services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__
)


@app.route("/routes")
def routes():

    return {
        "routes": sorted(
            [str(rule) for rule in app.url_map.iter_rules()]
        )
    }

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
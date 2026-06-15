from flask import Blueprint
from flask import jsonify

reports_bp = Blueprint(
    "reports",
    __name__
)

@reports_bp.route(
    "/inventory",
    methods=["GET"]
)
def inventory_report():

    return jsonify({
        "message":
        "Inventory report endpoint working"
    })
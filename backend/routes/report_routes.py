from flask import Blueprint
from flask import send_file
print("REPORT ROUTES LOADED")

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from models.product import Product

report_bp = Blueprint(
    "report",
    __name__
)


@report_bp.route(
    "/inventory",
    methods=["GET"]
)
def inventory_report():

    pdf_file = "inventory_report.pdf"

    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Inventory Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    products = Product.query.all()

    for product in products:

        elements.append(
            Paragraph(
                f"""
                {product.name}
                |
                Qty: {product.quantity}
                |
                Price: ₹{product.price}
                """,
                styles["BodyText"]
            )
        )

    doc.build(elements)

    return send_file(
        pdf_file,
        as_attachment=True
    )
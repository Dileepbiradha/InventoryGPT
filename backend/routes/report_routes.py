from flask import Blueprint
from flask import send_file

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from models.product import Product

reports_bp = Blueprint(
    "reports",
    __name__
)


@reports_bp.route(
    "/inventory",
    methods=["GET"]
)
def inventory_report():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Inventory Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    products = Product.query.all()

    for product in products:

        content.append(
            Paragraph(
                f"""
                <b>{product.name}</b><br/>
                SKU: {product.sku}<br/>
                Quantity: {product.quantity}<br/>
                Price: ₹{product.price}<br/>
                Supplier: {product.supplier}
                """,
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

    doc.build(content)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="inventory_report.pdf",
        mimetype="application/pdf"
    )
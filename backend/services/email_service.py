from flask_mail import Message
from extensions import mail


def send_low_stock_email(product):

    msg = Message(
        subject="Low Stock Alert",
        recipients=["admin@gmail.com"]
    )

    msg.body = f"""
Product: {product.name}

Current Stock: {product.quantity}

Minimum Stock: {product.minimum_stock}

Please reorder immediately.
"""

    mail.send(msg)
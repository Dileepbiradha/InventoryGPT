from extensions import db

from models.purchase_order import PurchaseOrder
from models.product import Product
from models.transaction import Transaction


class PurchaseOrderService:

    @staticmethod
    def approve_order(order_id):

        order = PurchaseOrder.query.get(order_id)

        if not order:
            raise ValueError(
                "Purchase order not found"
            )

        if order.status == "Approved":
            raise ValueError(
                "Purchase order already approved"
            )

        product = Product.query.get(
            order.product_id
        )

        if not product:
            raise ValueError(
                "Product not found"
            )

        # Update inventory
        product.quantity += order.quantity

        # Mark order approved
        order.status = "Approved"

        # Create inventory transaction record
        transaction = Transaction(
            product_id=product.id,
            quantity=order.quantity,
            transaction_type="IN"
        )

        db.session.add(transaction)

        db.session.commit()

        return order
from extensions import db

from models.product import Product
from models.transaction import Transaction
from models.purchase_order import PurchaseOrder


class InventoryService:

    @staticmethod
    def stock_in(product_id, quantity):

        product = Product.query.get(product_id)

        if not product:
            raise ValueError(
                "Product not found"
            )

        product.quantity += quantity

        transaction = Transaction(
            product_id=product.id,
            transaction_type="IN",
            quantity=quantity
        )

        db.session.add(transaction)
        db.session.commit()

        return product

    @staticmethod
    def stock_out(product_id, quantity):

        product = Product.query.get(product_id)

        if not product:
            raise ValueError(
                "Product not found"
            )

        if product.quantity < quantity:
            raise ValueError(
                "Insufficient stock"
            )

        product.quantity -= quantity

        transaction = Transaction(
            product_id=product.id,
            transaction_type="OUT",
            quantity=quantity
        )

        db.session.add(transaction)

        # AUTO REORDER

        minimum_stock = (
            product.minimum_stock or 20
        )

        if product.quantity < minimum_stock:

            existing_order = PurchaseOrder.query.filter_by(
                product_id=product.id,
                status="Pending"
            ).first()

            if not existing_order:

                purchase_order = PurchaseOrder(
                    product_id=product.id,
                    quantity=50,
                    supplier=product.supplier,
                    status="Pending"
                )

                db.session.add(
                    purchase_order
                )

        db.session.commit()

        return product
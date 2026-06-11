from extensions import db

from models.product import Product
from models.transaction import Transaction


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
        db.session.commit()

        return product
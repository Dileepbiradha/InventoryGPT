from models.product import Product
from extensions import db


class ProductService:

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def create(data):

        existing_product = Product.query.filter_by(
            sku=data["sku"]
        ).first()

        if existing_product:
            raise ValueError(
                "SKU already exists"
            )

        product = Product(
            name=data["name"],
            sku=data["sku"],
            category=data.get("category"),
            price=data["price"],
            quantity=data.get("quantity", 0),
            minimum_stock=data.get("minimum_stock", 20),
            supplier=data.get("supplier")
        )

        db.session.add(product)
        db.session.commit()

        return product

    @staticmethod
    def update(product, data):

        product.name = data.get(
            "name",
            product.name
        )

        product.sku = data.get(
            "sku",
            product.sku
        )

        product.category = data.get(
            "category",
            product.category
        )

        product.price = data.get(
            "price",
            product.price
        )

        product.quantity = data.get(
            "quantity",
            product.quantity
        )

        product.supplier = data.get(
            "supplier",
            product.supplier
        )

        db.session.commit()

        return product

    @staticmethod
    def delete(product):

        db.session.delete(product)
        db.session.commit()
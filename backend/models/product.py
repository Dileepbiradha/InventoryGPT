from datetime import datetime
from extensions import db


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    sku = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=0
    )

    minimum_stock = db.Column(
    db.Integer,
    default=20
    )

    supplier = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "minimum_stock": self.minimum_stock,
            "supplier": self.supplier,
            "created_at": self.created_at.isoformat()
        }
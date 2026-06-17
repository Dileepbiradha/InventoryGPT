from datetime import datetime

from extensions import db
from models.product import Product


class PurchaseOrder(db.Model):

    __tablename__ = "purchase_orders"

    product = db.relationship(
        "Product",
        backref="purchase_orders"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    supplier = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,

            "product_name":
                self.product.name
                if self.product
                else None,

            "quantity": self.quantity,

            "product":
                self.product.to_dict()
                if self.product
                else None,

            "supplier": self.supplier,

            "status": self.status,

            "created_at":
                self.created_at.isoformat()
        }
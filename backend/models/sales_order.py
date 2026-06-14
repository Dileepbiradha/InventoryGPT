from datetime import datetime
from extensions import db


class SalesOrder(db.Model):

    __tablename__ = "sales_orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
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

    total_amount = db.Column(
    db.Float,
    default=0
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    customer = db.relationship(
        "Customer",
        backref="sales_orders"
    )

    product = db.relationship(
        "Product",
        backref="sales_orders"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name":
                self.customer.name
                if self.customer else None,

            "product_id": self.product_id,
            "product_name":
                self.product.name
                if self.product else None,

            "quantity": self.quantity,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at":
                self.created_at.isoformat()
        }
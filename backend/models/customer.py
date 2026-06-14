from datetime import datetime
from extensions import db

class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(50)
    )

    address = db.Column(
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
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "created_at":
                self.created_at.isoformat()
        }
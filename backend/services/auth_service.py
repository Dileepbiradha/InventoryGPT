import bcrypt

from flask_jwt_extended import create_access_token

from models.user import User
from extensions import db


class AuthService:

    @staticmethod
    def register(data):

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            raise ValueError(
                "User already exists"
            )

        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"),
            bcrypt.gensalt()
        )

        user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password.decode("utf-8"),
            role=data.get("role", "staff")
        )

        db.session.add(user)
        db.session.commit()

        return user.to_dict()

    @staticmethod
    def login(data):

        user = User.query.filter_by(
            email=data["email"]
        ).first()

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        password_match = bcrypt.checkpw(
            data["password"].encode("utf-8"),
            user.password.encode("utf-8")
        )

        if not password_match:
            raise ValueError(
                "Invalid credentials"
            )

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return {
            "access_token": access_token,
            "user": user.to_dict()
        }
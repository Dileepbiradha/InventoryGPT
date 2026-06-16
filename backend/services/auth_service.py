import bcrypt

from models.user import User
from extensions import db


class AuthService:

    @staticmethod
    def login(data):

        print("LOGIN ATTEMPT:", data["email"])

        user = User.query.filter_by(
            email=data["email"]
        ).first()

        print("USER FOUND:", user)

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        password_match = bcrypt.checkpw(
            data["password"].encode("utf-8"),
            user.password.encode("utf-8")
        )

        print("PASSWORD MATCH:", password_match)

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
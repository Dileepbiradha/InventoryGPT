from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

class Config:

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "inventory.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
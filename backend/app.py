from flask import Flask

from config import Config
from extensions import db, migrate

from models.product import Product
from models.transaction import Transaction

from routes.inventory_routes import inventory_bp
from routes.product_routes import product_bp
from routes.dashboard_routes import dashboard_bp
from routes.ai_routes import ai_bp

from flask_cors import CORS


def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(
        product_bp,
        url_prefix="/api/products"
    )

    app.register_blueprint(
        dashboard_bp,
        url_prefix="/api/dashboard"
    )
    app.register_blueprint(
    inventory_bp,
    url_prefix="/api/inventory"
    )
    app.register_blueprint(
    ai_bp,
    url_prefix="/api/ai"
    )

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return {
            "error": str(error)
        }, 400

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

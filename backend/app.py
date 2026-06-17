from models.user import User
from routes.report_routes import reports_bp
from routes.product_routes import product_bp
from routes.dashboard_routes import dashboard_bp
from routes.analytics_routes import analytics_bp
from routes.supplier_routes import supplier_bp
from routes.sales_order_routes import sales_order_bp
from routes.customer_routes import customer_bp
from routes.low_stock_routes import low_stock_bp
from routes.ai_inventory_routes import ai_inventory_bp
from routes.transaction_routes import transaction_bp
from routes.purchase_order_routes import purchase_order_bp
from routes.auth_routes import auth_bp
from routes.inventory_routes import inventory_bp
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, mail, migrate, jwt

app = Flask(__name__)
app.config.from_object(Config)   # ← ADD THIS LINE

CORS(
    app,
    resources={r"/*": {"origins": [
        "https://inventorygpt-1.onrender.com",
        "http://localhost:5173"
    ]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
mail.init_app(app)
with app.app_context():
    db.create_all()

    
def debug_users():
    users = User.query.all()

    return {
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "password": u.password
            }
            for u in users
        ]
    }


@app.route("/routes")
def routes():
    return {
        "routes": sorted(
            [str(rule) for rule in app.url_map.iter_rules()]
        )
    }


@app.route("/")
def home():
    return {
        "status": "running",
        "cors": "enabled"
    }

app.register_blueprint(
    product_bp,
    url_prefix="/api/products"
)

app.register_blueprint(
    dashboard_bp,
    url_prefix="/api/dashboard"
)

app.register_blueprint(
    analytics_bp,
    url_prefix="/api/analytics"
)

app.register_blueprint(
    supplier_bp,
    url_prefix="/api/suppliers"
)


app.register_blueprint(
    sales_order_bp,
    url_prefix="/api/sales-orders"
)

app.register_blueprint(
    customer_bp,
    url_prefix="/api/customers"
)

app.register_blueprint(
    low_stock_bp,
    url_prefix="/api/low-stock"
)

app.register_blueprint(
    transaction_bp,
    url_prefix="/api/transactions"
)

app.register_blueprint(
    purchase_order_bp,
    url_prefix="/api/purchase-orders"
)

app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

app.register_blueprint(
    inventory_bp,
    url_prefix="/api/inventory"
)

app.register_blueprint(
    reports_bp,
    url_prefix="/api/reports"
)



app.register_blueprint(
    ai_inventory_bp,
    url_prefix="/api/ai-inventory"
)

if __name__ == "__main__":
    app.run(debug=True)
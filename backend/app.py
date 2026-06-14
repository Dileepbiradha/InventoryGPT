import os
# force railway redeploy
from routes.product_routes import product_bp
from routes.dashboard_routes import dashboard_bp
from routes.analytics_routes import analytics_bp
from routes.supplier_routes import supplier_bp
from routes.sales_order_routes import sales_order_bp
from routes.customer_routes import customer_bp
from routes.low_stock_routes import low_stock_bp
#from routes.ai_inventory_routes import ai_inventory_bp
from routes.transaction_routes import transaction_bp
from routes.purchase_order_routes import purchase_order_bp
from routes.auth_routes import auth_bp
from routes.inventory_routes import inventory_bp
from flask import Flask
from flask_cors import CORS

from config import Config

from extensions import (
    db,
    mail,
    migrate,
    jwt
)

app = Flask(__name__)

app.config.from_object(Config)

CORS(
    app,
    supports_credentials=True
)


# db.init_app(app)
# migrate.init_app(app, db)
# jwt.init_app(app)
# mail.init_app(app)

#app.register_blueprint(
#    product_bp,
#    url_prefix="/api/products"
#)

#app.register_blueprint(
#    dashboard_bp,
#    url_prefix="/api/dashboard"
#)

#app.register_blueprint(
#    analytics_bp,
#    url_prefix="/api/analytics"
#)

#app.register_blueprint(
#    supplier_bp,
#    url_prefix="/api/suppliers"
#)

#app.register_blueprint(
#    sales_order_bp,
#    url_prefix="/api/sales-orders"
#)

#app.register_blueprint(
#    customer_bp,
#    url_prefix="/api/customers"
#)

#app.register_blueprint(
#    low_stock_bp,
#    url_prefix="/api/low-stock"
#)

#app.register_blueprint(
#    transaction_bp,
#    url_prefix="/api/transactions"
#)

#app.register_blueprint(
#    ai_inventory_bp,
#    url_prefix="/api/ai-inventory"
#)

#app.register_blueprint(
#    purchase_order_bp,
#    url_prefix="/api/purchase-orders"
#)

#app.register_blueprint(
#    auth_bp,
#    url_prefix="/api/auth"
#)

#app.register_blueprint(
#    inventory_bp,
#    url_prefix="/api/inventory"
#)

@app.route("/")
def home():
    return {
        "status": "running",
        #"service": "InventoryGPT"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
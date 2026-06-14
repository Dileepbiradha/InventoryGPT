from models.product import Product
from models.sales_order import SalesOrder
from models.purchase_order import PurchaseOrder


def get_inventory_context():

    products = Product.query.all()

    context = "INVENTORY DATA\n\n"

    for product in products:

        context += f"""
Product: {product.name}
SKU: {product.sku}
Category: {product.category}
Quantity: {product.quantity}
Minimum Stock: {product.minimum_stock}
Price: {product.price}
Supplier: {product.supplier}

"""

    sales_orders = SalesOrder.query.all()

    context += "\nSALES ORDERS\n\n"

    for order in sales_orders:

        context += f"""
Sales Order ID: {order.id}
Product ID: {order.product_id}
Quantity: {order.quantity}
Status: {order.status}

"""

    purchase_orders = PurchaseOrder.query.all()

    context += "\nPURCHASE ORDERS\n\n"

    for order in purchase_orders:

        context += f"""
Purchase Order ID: {order.id}
Product ID: {order.product_id}
Quantity: {order.quantity}
Status: {order.status}

"""

    return context